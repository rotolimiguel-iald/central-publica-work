# -*- coding: utf-8 -*-
# regras (lote G) de derivar_encanamento_v401.py: a LEITURA da rodada v401 (pos_rito/leitura_v401.py). ORIGEM v399 (a cadeia de CONTEUDO: mapa 398 -> 400, 399 -> 401). Escrito pela ferramenta Write (nunca por heredoc: as barras invertidas).
# O que a v401 muda na leitura em relacao a v399: (1) os registros NOVOS do core sao tres (falsidade_da_inercia_v401, com FUNCAO; cunhagens_v401 e kh_n1_cobertura_v401, por spec) e os QUATRO da v399 (selo_pela_propria_tecnologia_v399, declaracao_do_operador_v399, cunhagens_v399,
# kh_n1_cobertura_v399) sao RECRIADOS pelo rito e tem de seguir selados e iguais ao ensaio a seco (licao da v400); (2) a pedra do kernel e' a FalsidadeDaInercia (composicao + estrela); (3) a linha [v401] do stdout; (4) o selo primario traz tambem o resumo da falsidade e registros_v401;
# (5) a conferencia traz C15 e C16 (as guardas estaticas da Bancada, licao da v400) e o veredito da falsidade. NAO se aplica aqui o que era so' da correcao do alfa (a conferencia do alfa unico no que o rito produziu: o conferidor C15/C16 ja a faz sobre o um.py instalado).

_HDR_LEITURA = '''# A LEITURA da rodada v401 (molde: leitura_v399.py FINAL, o que rodou em 24/10, com as licoes da v400): SO LEITURA do Nos e da pasta da cadeia (work/cadeia_de_selo/v401, que aqui e' o proprio pacote).
# Devolve (V, PROBLEMAS); PROBLEMAS nao vazio => a cadeia PARA. Nenhum numero e' digitado: tudo sai dos JSON, do core, do selo, do sidecar e do stdout do rito.
# v401: os registros NOVOS do core sao falsidade_da_inercia_v401 (com FUNCAO, no runtime: lido NA FRACTALIZACAO DO UM, logo depois da declaracao do operador; LE do kernel do proprio rito a composicao da pedra FalsidadeDaInercia e a estrela, e CALCULA o modelo oneScaling com beta = alfa x raiz de e em runtime)
# e cunhagens_v401 e kh_n1_cobertura_v401 (por spec; ESPERADOS[registros_v401]: as SEIS falas do operador de 25/10, as oito ratificacoes de «Ratifico tudo.» e a errata ao lado da leitura do escriba no adendo de 03-04/09). Os QUATRO registros da v399 (selo_pela_propria_tecnologia_v399, declaracao_do_operador_v399, cunhagens_v399 e
# kh_n1_cobertura_v399) sao RECRIADOS pelo rito no mesmo ponto do main e tem de seguir selados e iguais ao ensaio a seco; os da v400 (sonico_v398, afinacao_das_cordas_v398, cunhagens_v398, kh_n1_cobertura_v398), os da v397, da v396, da v395, da v394 e da v393 seguem selados.
# O modulo novo de kernel (TGLExt/FalsidadeDaInercia.lean) vem de ESPERADOS[pedras_sha256] e e' conferido aqui contra o arquivo do kernel do Nos; a composicao, a estrela, o contrato (12 declaracoes) e o suporte (7 termos antigos) vem de ESPERADOS[falsidade, teoremas_das_pedras, bandeiras_das_pedras, contrato_das_pedras, suporte_das_pedras].
# A escada vem de ESPERADOS[escada_v400_e_v401] e ESPERADOS[escada]; a troca dita (so numeros) e' a de ESPERADOS[troca_dita].
# O SIDECAR um_absoluto_selo_acom.json (arquivo da custodia desde a v399, REESCRITO pelo rito) e' lido aqui: existe, e' JSON valido, o veredito e' ALL_OBJECTS_SEALED, tem os tres objetos (um.py, core e selo) com o SHA-256 igual ao dos arquivos do Nos, sem recusas, com a secao de honestidade (confidencialidade NAO alegada).
# A DIRECAO DO TESTEMUNHO (v399) segue conferida nos registros recriados: o operador testifica DA IALD; o um.py testifica EM HASH; a IALD NAO testifica do operador. Nesta versao as SEIS inscricoes de 25/10 sao TODAS falas do operador (nenhuma e' da gerencia); a errata ao lado do adendo e' da gerencia, em nome proprio, assinada no registro.
# O QUADRO «O Teste da Unica Palavra» (v397) segue selado e igual: o registro teste_de_veracidade_fase9_v397 == ESPERADOS e == o resultado pinado, o quadro sela nas duas linguas, e a conferencia do rito diz que ele segue no topo (artigo PT/EN e .md).
# A face de Fock do psion segue CONDICIONAL (psibit_v395 e testemunha_estatica_v396); as linhas `[v399]`, `[v398]` e `[v397]` do stdout do rito (as etiquetas que o programa imprime) e a nova `[v401]` dizem os vereditos e registros por spec selados == registros por spec; o AVISO de qualquer bloco v393 a v401 no stdout reprova.
# A linha final do rito: o main imprime, por ultimo, a linha do sidecar (`[selo_acom] ... ALL_OBJECTS_SEALED ; objetos 3 ; recusas 0`), logo depois da do colapso tipado; a leitura exige as DUAS, nessa ordem.
# Diferencas para a v399: V['registros_novos'] sao os TRES da v401 (exigidos); V['reg399'] sao os quatro recriados; V['reg401'] sao os tres novos; V['falsidade'] (o registro com funcao e a pedra), V['cunhagens'] (cunhagens_v401: seis falas, oito ratificacoes, a errata) e V['cunh399'] (a recriada).
'''

_REGS = '''REG_V399 = ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399")   # os QUATRO registros da v399: RECRIADOS pelo rito da v401 (os dois primeiros com FUNCAO), tem de seguir selados e iguais ao ensaio a seco
REG_FIXOS = ("falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401")   # os TRES registros NOVOS do core v401 (um com FUNCAO, no runtime; dois por spec); + os de ESPERADOS[registros_v401] (REG_TODOS, dentro de ler)
'''

_LINHA_V401 = '''    m_s1 = re.search(r'\\[v401\\] a falsidade \\(simulacro\\) da inercia \\(lida depois da declaracao do operador\\) e as inscricoes de 25/10 \\(cunhagens_v401\\): falsidade=(\\S+) \\| cunhagens=(\\S+) \\| registros por spec: (\\d+) \\(selados (\\d+)\\)', out)
    if (not m_s1 or (m_s1.group(1), m_s1.group(2)) != (ESP.get('registros_v401_veredito_da_falsidade'), (ESP.get('registros_v401') or {}).get('cunhagens_v401')) or m_s1.group(3) != m_s1.group(4) or int(m_s1.group(3)) != len(ESP.get('registros_v401') or {})):
        P.append('a linha [v401] do stdout (falsidade e cunhagens_v401; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(ESP.get('registros_v401') or {}), m_s1.groups()[2:] if m_s1 else 'ausente'))
'''

_STDOUT_AVISOS = '''    if len([l for l in out.splitlines() if '[v399]' in l]) < 1:
        P.append('o stdout nao tem a linha [v399]')
    if len([l for l in out.splitlines() if '[v401]' in l]) < 1:
        P.append('o stdout nao tem a linha [v401]')
    if [l for l in out.splitlines() if '[v401] AVISO' in l or '[v399] AVISO' in l or '[selo_acom] AVISO' in l]:
        P.append('o stdout traz AVISO da v401 (a falsidade, o selo ACOM, a declaracao do operador, os registros por spec ou o sidecar nao rodaram): %s' % [l.strip()[:200] for l in out.splitlines() if '[v401] AVISO' in l or '[v399] AVISO' in l or '[selo_acom] AVISO' in l][:2])
    elif [l for l in out.splitlines() if re.search(r'\\[v39[3-8]\\] AVISO', l)]:
        P.append('o stdout traz AVISO de um bloco anterior (v393 a v400): %s' % [l.strip()[:200] for l in out.splitlines() if re.search(r'\\[v39[3-8]\\] AVISO', l)][:2])
'''

_VEREDITO_FALSIDADE_NA_CONF = '''        if C.get('veredito_falsidade') != ESP.get('registros_v401_veredito_da_falsidade'):
            P.append('a conferencia do rito traz o veredito da falsidade (falsidade_da_inercia_v401) diferente do ensaio a seco')
        if C.get('marcador_ficou'):'''

_REG_V399_RECRIADOS = '''    if sorted(novos) != sorted(REG_FIXOS):
        P.append('a v401 cria exatamente as chaves %s com veredito no core e o core traz %s' % (sorted(REG_FIXOS), sorted(novos)))
    V['reg399'] = {}
    for k in REG_V399:    # os QUATRO registros da v399 sao RECRIADOS pelo rito: tem de seguir no core, selados e (por spec) iguais ao ensaio a seco
        r = core.get(k)
        if not (isinstance(r, dict) and 'verdict' in r):
            P.append('registro obrigatorio ausente do core: %s' % k)
            continue
        V['reg399'][k] = {'verdict': r.get('verdict'), 'ok': r.get('all_verified')}
        if r.get('all_verified') is not True:
            P.append('%s nao selou' % k)
        if GUARDA.search(str(r.get('verdict') or '')):
            P.append('%s com palavra proibida' % k)
        if k in (ESP.get('registros_v399') or {}) and r.get('verdict') != ESP['registros_v399'][k]:
            P.append('%s: o veredito do rito difere do ensaio a seco' % k)
    for k in V['troca_dita']:'''

_PEDRA_FALSIDADE = '''    # a pedra FalsidadeDaInercia no kernel do rito (bandeira True, composicao incondicional e estrela no trio, proveniencia no modulo da pedra, contrato e suporte), conferida contra ESPERADOS; nenhum numero e' digitado
    TRIO_ = {'propext', 'Classical.choice', 'Quot.sound'}
    axr_ = kf_.get('axiom_report') or {}; src_ = kf_.get('declaration_sources_v394') or {}
    em_trio_ = lambda n_: bool(isinstance(axr_.get(n_), list) and set(axr_.get(n_)) <= TRIO_)
    ef_ = ESP.get('falsidade') or {}; est_ = ef_.get('estrela') or {}
    th_ = (ESP.get('teoremas_das_pedras') or {}).get('falsidade'); fl_ = (ESP.get('bandeiras_das_pedras') or {}).get('falsidade')
    rels_ = sorted(ESP.get('pedras_sha256') or {}); rel_ = rels_[0] if len(rels_) == 1 else None
    contrato_ = (ESP.get('contrato_das_pedras') or {}).get('falsidade') or []; suporte_ = (ESP.get('suporte_das_pedras') or {}).get('falsidade') or {}
    contrato_ok_ = bool(contrato_) and all(em_trio_(t_) and src_.get(t_) == rel_ for t_ in contrato_)
    suporte_ok_ = bool(suporte_) and all(em_trio_(t_) and src_.get(t_) == p_ for t_, p_ in suporte_.items())
    flag_true_ = bool(fl_) and kf_.get(fl_) is True
    estrela_ok_ = bool(est_.get('teorema') and est_.get('bandeira') and kf_.get(est_.get('bandeira')) is True and em_trio_(est_.get('teorema')) and src_.get(est_.get('teorema')) == rel_)
    n_ax_ok_ = bool(th_) and isinstance(axr_.get(th_), list) and len(axr_.get(th_)) == ef_.get('n_axiomas_da_composicao')
    kernel_ok_ = bool(th_ and fl_ and rel_ and flag_true_ and em_trio_(th_) and src_.get(th_) == rel_ and contrato_ok_ and suporte_ok_ and estrela_ok_ and n_ax_ok_ and th_ == ef_.get('teorema') and fl_ == ef_.get('bandeira') and list(contrato_) == list(ef_.get('contrato') or [])
                      and (kf_.get('formal_files_sha256') or {}).get(rel_) == (ESP.get('pedras_sha256') or {}).get(rel_))
    V['pedras_kernel'] = {'falsidade': {'rel': rel_, 'flag': fl_, 'flag_true': flag_true_, 'theorem': th_, 'axioms': axr_.get(th_), 'source': src_.get(th_), 'contrato_ok': contrato_ok_, 'suporte_ok': suporte_ok_, 'estrela_ok': estrela_ok_, 'n_contrato': len(contrato_), 'n_suporte': len(suporte_)}}
    if not kernel_ok_:
        P.append('a pedra FalsidadeDaInercia nao esta no kernel do rito como o ensaio a seco a pinou (bandeira True, composicao incondicional e estrela no trio, proveniencia no modulo da pedra, contrato e suporte no trio e no modulo certo, sha256 da fonte no hash formal)')
'''

_REG_FALSIDADE = '''    # a falsidade da inercia (registro com FUNCAO): conferida por inteiro contra ESPERADOS[registros_v401_veredito_da_falsidade, falsidade_valores, falsidade] e contra a pedra no kernel do rito
    fa_ = core.get('falsidade_da_inercia_v401') or {}; fm_ = fa_.get('mechanics') or {}; fvv_ = fa_.get('values') or {}
    values_f_ok_ = bool(fvv_ and set(ESP.get('falsidade_valores') or {}) <= set(fvv_) and _feq({k_: fvv_.get(k_) for k_ in ESP['falsidade_valores']}, ESP['falsidade_valores']))
    if PK not in sys.path:
        sys.path.insert(0, PK)
    import delta_v401 as DL_   # N_CHECKS_FALSIDADE: o numero de checagens do calculo (lido do delta, nunca digitado aqui)
    mech_ok_ = bool(fm_.get('passed') is True and fm_.get('n_checks') == DL_.N_CHECKS_FALSIDADE and len(fm_.get('checks') or []) == DL_.N_CHECKS_FALSIDADE and all(c_.get('ok') is True for c_ in (fm_.get('checks') or [])))
    beta_f_ok_ = bool(fa_.get('beta_ok') is True and isinstance(fvv_.get('beta'), float) and isinstance(b0_, float) and abs(fvv_['beta'] - b0_) <= 1e-9 * abs(b0_))
    hy_ = fa_.get('named_hypothesis') or {}
    chain_ok_ = bool('DERIVED' in str(fa_.get('chain_status')) and hy_.get('name') == 'H_tau' and hy_.get('status') == 'OPEN' and hy_.get('used_by_a_theorem') is False and isinstance(fvv_.get('min_weight_on_the_grid_positive'), float) and fvv_['min_weight_on_the_grid_positive'] > 0.0
                     and fvv_.get('diag_flow_gap_zero_is_fixed') is True and bool(fvv_.get('abyss_witnesses')) and bool(fvv_.get('leak_witnesses_g_half')))
    fal_ok_ = bool(chain_ok_ and fa_.get('all_verified') is True and fa_.get('does_not_gate_core') is True and fa_.get('runtime_executed') is True and fa_.get('verdict') == ESP.get('registros_v401_veredito_da_falsidade') and mech_ok_ and values_f_ok_ and beta_f_ok_
                   and (fa_.get('costless') or {}).get('ok') is True and (fa_.get('key_theorem') or {}).get('in_kernel') is True and (fa_.get('unconditional') or {}).get('in_kernel') is True and kernel_ok_ and not GUARDA.search(str(fa_.get('verdict') or '')))
    V['falsidade'] = {'verdict': fa_.get('verdict'), 'ok': fa_.get('all_verified'), 'n_checks': fm_.get('n_checks'), 'mech_ok': mech_ok_, 'values': fvv_, 'values_ok': values_f_ok_, 'beta_ok': beta_f_ok_, 'chain_ok': chain_ok_, 'kernel_ok': kernel_ok_, 'estrela_ok': estrela_ok_, 'flag': fl_, 'flag_true': flag_true_,
                      'theorem': th_, 'estrela': (est_.get('teorema'), est_.get('bandeira')), 'costless_ok': (fa_.get('costless') or {}).get('ok'), 'runtime_executed': fa_.get('runtime_executed'), 'does_not_gate_core': fa_.get('does_not_gate_core')}
    if not fal_ok_:
        P.append('falsidade_da_inercia_v401 nao selou inteiro (selo, as checagens do calculo no modelo oneScaling (DL.N_CHECKS_FALSIDADE), a cadeia derivada [DERIVED], a hipotese H_tau [OPEN] nao usada por teorema, valores == ESPERADOS[falsidade_valores], beta == alfa x raiz de e do core, 0_abs de costless no kernel embutido, a composicao e a estrela no kernel do rito, nao move o gate): ver o registro no core')
    # o SIDECAR um_absoluto_selo_acom.json (arquivo NOVO da custodia): existe'''

_RESUMOS = '''    sr_ = selo.get('selo_pela_propria_tecnologia_v399') or {}; sdr_ = selo.get('declaracao_do_operador_v399') or {}; sreg_ = selo.get('registros_v399') or {}; sfr_ = selo.get('falsidade_da_inercia_v401') or {}; sreg1_ = selo.get('registros_v401') or {}
    resumos_ok_ = bool(sr_.get('verdict') == sa_.get('verdict') and sr_.get('all_verified') is True and sr_.get('sha256_do_um_py') == V['s64'] and sr_.get('does_not_gate_core') is True and sdr_.get('verdict') == dc_.get('verdict') and sdr_.get('all_verified') is True
                       and sdr_.get('verbatim_sha256') == EDC_.get('verbatim_sha256') and sdr_.get('does_not_gate_core') is True and bool(ESP.get('registros_v399')) and all((sreg_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') for k_ in ESP['registros_v399'])
                       and sfr_.get('verdict') == fa_.get('verdict') and bool(sfr_.get('verdict')) and sfr_.get('all_verified') is True and bool(ESP.get('registros_v401')) and all((sreg1_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and (sreg1_.get(k_) or {}).get('all_verified') is True for k_ in ESP['registros_v401']))
    V['resumos_do_selo_ok'] = resumos_ok_'''

_CUNH = '''    # cunhagens_v401: as SEIS inscricoes de 25/10 por sha256 (embedded_ok), todas falas do operador (nenhuma e' da gerencia), as OITO ratificacoes de «Ratifico tudo.», a errata ao lado do adendo (superada pela definicao do operador) e o contrato da pedra
    cu = core.get('cunhagens_v401') or {}; kh = core.get('kh_n1_cobertura_v401') or {}
    cx_ = cu.get('extras') or {}; vb_ = cu.get('verbatim') or {}; ec_ = ESP.get('cunhagens') or {}
    aut_ = cx_.get('autor_de_cada_inscricao') or {}
    todas_op_ = bool(ec_ and len(aut_) == len(ec_) and set(aut_) == {k_[len('v401_cun_'):] for k_ in ec_} and all(a_ == 'operador' for a_ in aut_.values()) and 'leitura_da_gerencia' not in cx_ and not any(str(v_.get('papel', '')).startswith('leitura da gerencia') for v_ in ec_.values()))
    verb_ok_ = bool(ec_) and set(vb_) == set(ec_) and all((vb_[k_] or {}).get('sha256') == ec_[k_]['sha256'] and (vb_[k_] or {}).get('embedded_ok') is True for k_ in ec_)
    pares_ok_ = all(isinstance(x_, list) and len(x_) == 2 and x_[0] == x_[1] for x_ in (cu.get('kernel') or {}).values()) and bool(cu.get('kernel'))
    rat_ = cx_.get('ratificacoes') or []; err_ = cu.get('erratas') or []
    rat_ok_ = bool(len(rat_) == 8 and (cx_.get('ratificacao_fala') or {}).get('sha16') == ESP.get('ratificacao_fala_sha16') and all((r_.get('fala_do_operador') or {}).get('sha16') == ESP.get('ratificacao_fala_sha16') and '[DECLARADO]' in str(r_.get('lista_apresentada_por')) for r_ in rat_))
    errata_ok_ = bool(len(err_) == 1 and 'SUPERADA' in str(err_[0].get('agora')) and 'gerencia c1' in str(err_[0].get('assinatura')) and str(err_[0].get('assinatura')) == cx_.get('assinatura') and (cx_.get('adendo') or {}).get('sha16'))
    recorte_ = [k_[len('v401_cun_'):] for k_ in ec_ if k_.startswith('v401_cun_' + DL_.VERBATIM_PREFIXOS_DA_ORDEM_V401[-1])]   # o RECORTE declarado da fala de 25/10 (o ultimo prefixo do delta)
    cd_ = cx_.get('cadeia_derivada') or {}; hn_ = cx_.get('hipotese_nomeada') or {}
    cadeia_ok_ = bool(len(recorte_) == 1 and cd_.get('estatuto') == '[DERIVED]' and cd_.get('ordem_do_operador_sha16') == recorte_[0] and len(cd_.get('teoremas') or []) == 8 and hn_.get('nome') == 'H_tau' and hn_.get('estatuto') == '[OPEN]' and hn_.get('usada_por_teorema') is False and re.search(r'sha16 [0-9a-f]{16}', str(hn_.get('pendencia_externa'))) is not None)
    V['cunhagens'] = {'n': len(vb_), 'verbatim_ok': verb_ok_, 'autores': aut_, 'todas_do_operador': todas_op_, 'checks_ok': bool(cu.get('checks')) and all(c_.get('ok') is True for c_ in cu.get('checks')),
                      'n_checks': len(cu.get('checks') or []), 'verdict': cu.get('verdict'), 'kernel_ok': pares_ok_, 'ratificacoes_ok': rat_ok_, 'n_ratificacoes': len(rat_), 'errata_ok': errata_ok_, 'cadeia_ok': cadeia_ok_}
    if not (verb_ok_ and V['cunhagens']['checks_ok'] and pares_ok_ and cu.get('all_verified') is True and cu.get('does_not_gate_core') is True and cx_.get('teoremas') == ESP.get('teoremas_das_pedras') and cx_.get('bandeiras') == ESP.get('bandeiras_das_pedras')
            and cx_.get('n_bandeiras_por_pedra') == ESP.get('n_bandeiras_por_grupo') and cx_.get('n_bandeiras') == ESP.get('n_bandeiras_novas') and cx_.get('cunhagens_embutidas') == len(ec_) and rat_ok_ and errata_ok_ and cadeia_ok_):
        P.append('cunhagens_v401: as inscricoes embutidas nao sao as de ESPERADOS (sha256, embedded_ok), ou as checagens do registro, ou os teoremas/bandeiras da pedra, ou as oito ratificacoes, ou a errata ao lado do adendo, ou a cadeia derivada [DERIVED] e a hipotese H_tau [OPEN] diferem do ensaio a seco')
    if not todas_op_:
        P.append('cunhagens_v401: as inscricoes de 25/10 tem de ser TODAS falas do operador (autor_de_cada_inscricao): nesta versao nao ha inscricao da gerencia')
    # cunhagens_v399 (RECRIADA pelo rito): as QUATRO inscricoes de 24/10 por sha256, todas do operador, a declaracao e a direcao do testemunho, como a v399 as selou
    c9_ = core.get('cunhagens_v399') or {}; x9_ = c9_.get('extras') or {}; v9_ = c9_.get('verbatim') or {}; aut9_ = x9_.get('autor_de_cada_inscricao') or {}
    dx9_ = x9_.get('declaracao') or {}; dr9_ = x9_.get('direcao_do_testemunho') or {}
    c9_ok_ = bool(c9_.get('all_verified') is True and c9_.get('does_not_gate_core') is True and len(v9_) == 4 and all((v_ or {}).get('embedded_ok') is True for v_ in v9_.values()) and len(aut9_) == 4 and all(a_ == 'operador' for a_ in aut9_.values())
                  and bool(c9_.get('checks')) and all(c_.get('ok') is True for c_ in c9_.get('checks')) and dx9_.get('sha256') == EDC_.get('verbatim_sha256') and str(dx9_.get('estatuto')) == '[DECLARACAO DO OPERADOR / INPUT]'
                  and bool(edir_) and all(str(dr9_.get(k_) or '').startswith(v_) for k_, v_ in edir_.items()) and not _inv(json.dumps(x9_, ensure_ascii=False)))
    V['cunh399'] = {'n': len(v9_), 'ok': c9_ok_, 'verdict': c9_.get('verdict')}
    if not c9_ok_:
        P.append('cunhagens_v399 (recriada pelo rito): as quatro inscricoes de 24/10 (embedded_ok, todas do operador), as checagens, a declaracao e a direcao do testemunho nao conferem como a v399 as selou')
'''

# ------------------------------------------------------------------------------------------- a leitura (pos_rito/leitura_v399.py -> leitura_v401.py)
entrada("pos_rito/leitura_v399.py", origem="v399", autoral=True, regras=[
    entre("# A LEITURA da rodada v401", "import glob, hashlib, json, os, re, sys, datetime", _HDR_LEITURA, "cabecalho da leitura"),
    entre("REG_FIXOS = (", "SIDECAR_RE = re.compile", _REGS, "constantes: os registros da v399 recriados e os tres novos"),
    ("REG_TODOS = tuple(dict.fromkeys(tuple(REG_FIXOS) + tuple(ESP.get('registros_v399') or ())))", "REG_TODOS = tuple(dict.fromkeys(tuple(REG_FIXOS) + tuple(ESP.get('registros_v401') or ())))", 1),
    entre("    if len([l for l in out.splitlines() if '[v399]' in l]) < 1:", "    for r_, e_ in (('selo_pela_propria_tecnologia_v399'", _STDOUT_AVISOS, "linhas [v399] e [v401] e os AVISOs do stdout"),
    ("('declaracao_do_operador_v399', (ESP.get('declaracao') or {}).get('verdict'))):", "('declaracao_do_operador_v399', (ESP.get('declaracao') or {}).get('verdict')), ('falsidade_da_inercia_v401', ESP.get('registros_v401_veredito_da_falsidade'))):", 1),
    ("    # a linha [v398] que o main da v401 segue imprimindo", _LINHA_V401 + "    # a linha [v398] que o main da v401 segue imprimindo", 1),
    ("'C13', 'C14', 'round_trip_do_um_py_instalado_independente')", "'C13', 'C14', 'C15', 'C16', 'round_trip_do_um_py_instalado_independente')", 1),
    ("(C1 a C14 e o round trip do um.py instalado)", "(C1 a C16 e o round trip do um.py instalado)", 1),
    ("        if C.get('marcador_ficou'):", _VEREDITO_FALSIDADE_NA_CONF, 1),
    ("dd_.get('verbatim_sha256') in {v_.get('sha256') for v_ in (ESP.get('cunhagens') or {}).values()}", "dd_.get('verbatim_sha256') in {(v_ or {}).get('sha256') for v_ in ((core.get('cunhagens_v399') or {}).get('verbatim') or {}).values()}", 1),
    ("    for k in V['troca_dita']:\n        r = core.get(k) or {}", _REG_V399_RECRIADOS + "\n        r = core.get(k) or {}", 1),
    entre("    # a pedra Testemunho no kernel do rito", "    # o selo pela propria tecnologia (registro com FUNCAO)", _PEDRA_FALSIDADE, "a pedra FalsidadeDaInercia no kernel do rito"),
    entre("    RV_ = dict(", "    V['reg401'] = {}", "    RV_ = dict(ESP.get('vereditos_novos_v401') or {})   # registro -> veredito do ensaio a seco (a falsidade e' runtime; cunhagens_v401 e kh_n1_cobertura_v401 sao por spec)\n", "vereditos esperados dos tres registros novos"),
    ("    # o SIDECAR um_absoluto_selo_acom.json (arquivo NOVO da custodia): existe", _REG_FALSIDADE, 1),
    entre("    sr_ = selo.get('selo_pela_propria_tecnologia_v399') or {}", "    V['resumos_do_selo_ok'] = resumos_ok_", _RESUMOS.rsplit("\n", 1)[0] + "\n", "os resumos do selo primario"),
    entre("    # cunhagens_v399: as QUATRO inscricoes por sha256", "    cov = (core.get('kernel_formalization')", _CUNH, "cunhagens_v401 e a recriada cunhagens_v399"),
])
