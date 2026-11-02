# -*- coding: utf-8 -*-
"""adaptar_pos_rito_v405.py -- adapta ao CONTEUDO da v405 os scripts do pos-rito que derivar_encanamento_v405.py (lote F) gravou por subida de versao: regras de contagem exata (aborta se uma ancora nao casar o numero esperado de vezes), backup de bytes antes de tocar, temporario -> conferir -> substituir.
Opera sobre a SEMENTE: le de <arquivo>.semente_lote_F (a copia gravada na primeira execucao) e regrava o arquivo; assim e' reexecutavel sem acumular. Escrito pela ferramenta Write (barras invertidas e apostrofos nao passam pelo heredoc). Molde: a adaptacao a mao da gerencia em 28/10 (v404).
Nada executa o rito; nada toca o Nos. uso: python -I -B -X utf8 adaptar_pos_rito_v405.py [arquivo ...]"""
import ast, datetime, os, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
ARQS = {}


def regras(nome):
    def deco(f):
        ARQS[nome] = f
        return f
    return deco


class T:
    def __init__(s, txt, nome):
        s.t = txt; s.n = nome

    def sub(s, a, c, n=1):
        assert s.t.count(a) == n, ("ANCORA", s.n, a[:140], s.t.count(a), n)
        s.t = s.t.replace(a, c)

    def entre(s, ini, fim, novo):
        assert s.t.count(ini) == 1, ("ANCORA ini", s.n, ini[:120], s.t.count(ini))
        i = s.t.index(ini); j = s.t.index(fim, i + len(ini))
        s.t = s.t[:i] + novo + s.t[j:]


_OITO = ("ponte_da_massa_v405", "massa_tensao_pura_v405", "identidade_v405", "observador_terminal_v405", "lei_do_diminuto_v405", "tonica_do_hamiltoniano_v405", "disco_de_euler_v405", "ponto_zero_do_psion_v405")
_OITO_T = ", ".join('"%s"' % n_ for n_ in _OITO)
_KEYS = ("ponte", "tensao", "identidade", "observador", "diminuto", "tonica", "disco", "psion")
_PEDRA_DE = "{" + ", ".join('"%s": "%s"' % (k_, n_) for k_, n_ in zip(_KEYS, _OITO)) + "}"


@regras("leitura_v405.py")
def _leitura(x):
    x.sub('REG_FUNCAO = ("projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404")   # os TRES registros NOVOS com FUNCAO (no runtime; o ultimo, a errata de F2b, nao tem pedra)\n',
          'REG_V404B = ("projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "cunhagens_v404", "kh_n1_cobertura_v404")   # os CINCO registros da v404 SELADA: RECRIADOS pelo rito da v405, tem de seguir selados e iguais ao ensaio a seco (e a v404 selada)\n'
          'FUN_V404B = {"projecao": "projecao_transversal_v404", "jo8v32": "jo8v32_v404"}   # os DOIS registros com FUNCAO das pedras da v404 (recriados); a errata de F2b e\' lida a parte (V[\'f2b\'])\n'
          'REG_FUNCAO = (' + _OITO_T + ')   # os OITO registros NOVOS com FUNCAO (um por pedra)\n')
    x.sub('REG_FIXOS = REG_FUNCAO + ("cunhagens_v404", "kh_n1_cobertura_v404")   # os CINCO registros NOVOS do core v405 (tres com FUNCAO, dois por spec); + os de ESPERADOS[registros_v404] (REG_TODOS, dentro de ler)',
          'REG_FIXOS = REG_FUNCAO + ("cunhagens_v405", "campos_fechados_e_leituras_v405", "ga_reclassificacao_v405", "gap_v405", "kh_n1_cobertura_v405")   # os TREZE registros NOVOS do core v405 (oito com FUNCAO, cinco por spec); + os de ESPERADOS[registros_v405] (REG_TODOS, dentro de ler)')
    x.sub('PEDRA_DE = {"projecao": "projecao_transversal_v404", "jo8v32": "jo8v32_v404"}   # chave da pedra', 'PEDRA_DE = ' + _PEDRA_DE + '   # chave da pedra')
    x.sub("REG_TODOS = tuple(dict.fromkeys(tuple(REG_FIXOS) + tuple(ESP.get('registros_v404') or ())))", "REG_TODOS = tuple(dict.fromkeys(tuple(REG_FIXOS) + tuple(ESP.get('registros_v405') or ())))")
    x.sub("    RF_ = ESP.get('registros_funcao_v405') or {}   # projecao|jo8v32|f2b -> {nome, verdict, values, n_checks} do ensaio a seco\n", "    RF_ = ESP.get('registros_funcao_v405') or {}   # as oito chaves das pedras -> {nome, verdict, values, n_checks} do ensaio a seco\n    RF4_ = ESP.get('registros_funcao_v404') or {}   # projecao|jo8v32|f2b -> o mesmo, dos registros da v404 SELADA (recriados pelo rito da v405)\n")
    x.sub("    RF3_ = ESP.get('registros_funcao_v404') or {}   # caminho|vida|verdade_adendo|gate -> o mesmo, dos registros da v404 (recriados pelo rito da v405)\n", "    RF3_ = ESP.get('registros_funcao_v403') or {}   # caminho|vida|verdade_adendo|gate -> o mesmo, dos registros da v403 (recriados pelo rito da v405)\n")
    # os registros da v404 recriados, no ponto em que a leitura confere os recriados
    x.sub("    V['reg399'] = {}\n    for k in REG_V399:", "    V['reg404b'] = {}\n"
          "    for k in REG_V404B:    # os CINCO registros da v404 SELADA sao RECRIADOS pelo rito: seguem no core, selados e iguais ao selado\n"
          "        r = core.get(k)\n"
          "        if not (isinstance(r, dict) and 'verdict' in r):\n"
          "            P.append('registro obrigatorio ausente do core: %s' % k)\n"
          "            continue\n"
          "        V['reg404b'][k] = {'verdict': r.get('verdict'), 'ok': r.get('all_verified')}\n"
          "        if r.get('all_verified') is not True:\n"
          "            P.append('%s nao selou' % k)\n"
          "        if GUARDA.search(str(r.get('verdict') or '')):\n"
          "            P.append('%s com palavra proibida' % k)\n"
          "        if k in (ESP.get('vereditos_v404') or {}) and k not in (ESP.get('troca_dita') or []) and r.get('verdict') != ESP['vereditos_v404'][k]:\n"
          "            P.append('%s: o veredito do rito difere do ensaio a seco (a v404 selada)' % k)\n"
          "    V['reg399'] = {}\n    for k in REG_V399:")
    x.sub("    fb_ = core.get('f2b_errata_v404') or {}; EFB_ = RF_.get('f2b') or {};", "    fb_ = core.get('f2b_errata_v404') or {}; EFB_ = RF4_.get('f2b') or {};")
    x.sub("f2b_mech_ok_ = bool(fbm_.get('passed') is True and fbm_.get('n_checks') == DL_.N_CHECKS['f2b'] == EFB_.get('n_checks') and len(fbm_.get('checks') or []) == DL_.N_CHECKS['f2b'] and", "f2b_mech_ok_ = bool(fbm_.get('passed') is True and fbm_.get('n_checks') == DL_.D4.N_CHECKS['f2b'] == EFB_.get('n_checks') and len(fbm_.get('checks') or []) == DL_.D4.N_CHECKS['f2b'] and")
    x.sub("fb_.get('F2b_status_now') == DL_.F2B_FUTURO_TOKEN == (ESP.get('f2b_depois') or {}).get('F2b_status_now') and fb_.get('channel_token_now') == DL_.F2B_FUTURO_TOKEN and fb_.get('v1_token_kept') == DL_.F2B_V1_TOKEN_ANTIGO", "fb_.get('F2b_status_now') == DL_.D4.F2B_FUTURO_TOKEN == (ESP.get('f2b_depois') or {}).get('F2b_status_now') and fb_.get('channel_token_now') == DL_.D4.F2B_FUTURO_TOKEN and fb_.get('v1_token_kept') == DL_.D4.F2B_V1_TOKEN_ANTIGO")
    x.sub("valores == ESPERADOS[registros_funcao_v405][f2b]", "valores == ESPERADOS[registros_funcao_v404][f2b]")
    x.sub("nenhum desfecho, nao move o gate): ver o registro no core' % DL_.N_CHECKS['f2b'])", "nenhum desfecho, nao move o gate): ver o registro no core' % DL_.D4.N_CHECKS['f2b'])")
    x.sub("    for fkey_, FUN_ in (('fun402', FUN_V402), ('fun404', FUN_V404)):", "    for fkey_, FUN_ in (('fun402', FUN_V402), ('fun404', FUN_V404), ('fun404b', FUN_V404B)):")
    x.sub("    if len(V['pedras_v404']) != 3 or any(p_['ok'] is not True for p_ in V['pedras_v404'].values()):", "    if len(V['pedras_v404']) != 5 or any(p_['ok'] is not True for p_ in V['pedras_v404'].values()):")
    # os resumos do selo: os oito e registros_v405
    x.sub("sreg4_ = selo.get('registros_v404') or {}\n", "sreg4_ = selo.get('registros_v404') or {}; sreg5_ = selo.get('registros_v405') or {}\n")
    x.sub("for n_ in tuple(REG_FUNCAO) + tuple(FUN_V404.values()) + tuple(FUN_V402.values()) + ('bandeiras_do_gate_v403',))", "for n_ in tuple(REG_FUNCAO) + tuple(FUN_V404B.values()) + ('f2b_errata_v404',) + tuple(FUN_V404.values()) + tuple(FUN_V402.values()) + ('bandeiras_do_gate_v403',))")
    x.sub("                       and bool(ESP.get('registros_v404')) and all((sreg4_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg4_.get(k_) or {}).get('verdict')) and (sreg4_.get(k_) or {}).get('all_verified') is True for k_ in ESP['registros_v404']))\n",
          "                       and bool(ESP.get('registros_v404')) and all((sreg4_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg4_.get(k_) or {}).get('verdict')) and (sreg4_.get(k_) or {}).get('all_verified') is True for k_ in ESP['registros_v404'])\n"
          "                       and bool(ESP.get('registros_v405')) and all((sreg5_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg5_.get(k_) or {}).get('verdict')) and (sreg5_.get(k_) or {}).get('all_verified') is True for k_ in ESP['registros_v405']))\n")
    # as cunhagens da v405 e o registro dos campos fechados
    x.entre("    # cunhagens_v404: as NOVE falas do operador de 28/10 por sha256", "    # cunhagens_v403 e kh_n1_cobertura_v403 (RECRIADOS pelo rito, por spec)", _BLOCO_CUNH_V405)
    x.sub("    # a face de Fock do psion segue como a v395 a selou: CONDICIONAL, sem habitante exibido, com a bandeira True e declarada em Psibit.lean (nem a v396, nem a v397, nem a v404, nem a v405 a habitam)\n", "    # a face de Fock do psion segue como a v395 a selou: CONDICIONAL, sem habitante exibido, com a bandeira True e declarada em Psibit.lean (nem a v396, nem a v397, nem a v404, nem a v405 a habitam)\n")


_BLOCO_CUNH_V405 = r'''    # cunhagens_v405: as falas do operador de 30/10 a 01/11 por sha256 (embedded_ok), todas do operador, as erratas E10 a E13 (gerencia c1, em nome proprio), as decisoes D27 a D33, os nomes das oito pedras, a leitura da v405 e o contrato das pedras
    cu = core.get('cunhagens_v405') or {}; kh = core.get('kh_n1_cobertura_v405') or {}
    cx_ = cu.get('extras') or {}; vb_ = cu.get('verbatim') or {}; ec_ = ESP.get('cunhagens') or {}
    aut_ = cx_.get('autor_de_cada_inscricao') or {}; pref_ = DL_.VERBATIM_CHAVE_PREFIXO_V405
    todas_op_ = bool(ec_ and len(aut_) == len(ec_) and set(aut_) == {k_[len(pref_):] for k_ in ec_} and all(a_ == 'operador' for a_ in aut_.values()) and 'leitura_da_gerencia' not in cx_ and not any(str(v_.get('papel', '')).startswith('leitura da gerencia') for v_ in ec_.values()))
    verb_ok_ = bool(ec_) and set(vb_) == set(ec_) and all((vb_[k_] or {}).get('sha256') == ec_[k_]['sha256'] and (vb_[k_] or {}).get('embedded_ok') is True for k_ in ec_)
    pares_ok_ = all(isinstance(x_, list) and len(x_) == 2 and x_[0] == x_[1] for x_ in (cu.get('kernel') or {}).values()) and bool(cu.get('kernel'))
    err_ = cu.get('erratas') or []; esp_err_ = list(ESP.get('erratas_E10_a_E13') or [])
    erratas_ok_ = bool(len(err_) == len(esp_err_) == len(DL_.ERRATAS_V405) == 4 and all(str(e_.get('assinatura', '')).startswith('gerencia c1, em nome proprio') for e_ in err_) and [e_.get('agora') for e_ in err_] == esp_err_
                       and cx_.get('erratas_E10_a_E13') == esp_err_ and str(cx_.get('assinatura', '')).startswith('gerencia c1, em nome proprio'))
    dec_ = cx_.get('decisoes_da_gerencia') or {}; exig_ = {'D%d' % i_ for i_ in range(27, 34)}
    decisoes_ok_ = bool(set(dec_) >= exig_ and dec_ == (ESP.get('decisoes_da_gerencia') or {None: None}) and all(str(dec_.get(d_) or '').strip() for d_ in exig_))
    nm_ = cx_.get('nomes') or {}
    nomes_ok_ = bool(all(str(nm_.get(k_) or '').strip() for k_ in PEDRA_DE))
    ms_ = cx_.get('leitura_v405') or {}; ems_ = ESP.get('leitura_v405') or {}
    massa_ok_ = bool(ems_ and ms_ == ems_)
    pv405_ = cx_.get('pedras_da_v404_como_registro') or {}; rels405_ = {'projecao': 'TGLExt/ProjecaoTransversalDaMeiaNat.lean', 'jo8v32': 'TGLExt/Jo8v32.lean'}
    reg404_ok_ = bool(set(pv405_) == set(rels405_) and all(r_ in (ESP.get('pedras_v404_sha256') or {}) for r_ in rels405_.values()) and all(pv405_.get(k_) == (ESP['pedras_v404_sha256'][r_])[:16] for k_, r_ in rels405_.items()))
    teor_ok_ = bool(cx_.get('teoremas') == ESP.get('teoremas_das_pedras') and cx_.get('bandeiras') == ESP.get('bandeiras_das_pedras') and cx_.get('n_bandeiras_por_pedra') == ESP.get('n_bandeiras_por_grupo') and cx_.get('n_bandeiras') == ESP.get('n_bandeiras_novas')
                    and cx_.get('cunhagens_embutidas') == len(ec_) and {k_: (v_ or {}).get('teorema') for k_, v_ in (ESP.get('estrelas_v405') or {}).items()} == cx_.get('estrelas'))
    kh_ok_ = bool(kh.get('all_verified') is True and kh.get('does_not_gate_core') is True and bool((ESP.get('registros_v405') or {}).get('kh_n1_cobertura_v405')) and kh.get('verdict') == (ESP.get('registros_v405') or {}).get('kh_n1_cobertura_v405'))
    checks_cu_ok_ = bool(cu.get('checks')) and all(c_.get('ok') is True for c_ in cu.get('checks'))
    cu_ok_ = bool(verb_ok_ and checks_cu_ok_ and pares_ok_ and cu.get('all_verified') is True and cu.get('does_not_gate_core') is True and teor_ok_ and erratas_ok_ and decisoes_ok_ and nomes_ok_ and massa_ok_ and reg404_ok_ and todas_op_ and cu.get('verdict') == (ESP.get('registros_v405') or {}).get('cunhagens_v405') and not GUARDA.search(str(cu.get('verdict') or '')))
    V['cunhagens'] = {'n': len(vb_), 'ok': cu_ok_, 'verbatim_ok': verb_ok_, 'autores': aut_, 'todas_do_operador': todas_op_, 'checks_ok': checks_cu_ok_, 'n_checks': len(cu.get('checks') or []), 'verdict': cu.get('verdict'), 'kernel_ok': pares_ok_, 'erratas_ok': erratas_ok_, 'n_erratas': len(err_),
                      'decisoes_ok': decisoes_ok_, 'n_decisoes': len(dec_), 'nomes_ok': nomes_ok_, 'massa_ok': massa_ok_, 'reg404_ok': reg404_ok_, 'teoremas_ok': teor_ok_, 'kh_ok': kh_ok_}
    V['n_bandeiras'] = cx_.get('n_bandeiras'); V['n_bandeiras_por_pedra'] = cx_.get('n_bandeiras_por_pedra')
    if not (verb_ok_ and checks_cu_ok_ and pares_ok_ and cu.get('all_verified') is True and cu.get('does_not_gate_core') is True and teor_ok_ and cu.get('verdict') == (ESP.get('registros_v405') or {}).get('cunhagens_v405')):
        P.append('cunhagens_v405: as inscricoes embutidas nao sao as de ESPERADOS (sha256, embedded_ok), ou as checagens do registro, ou os teoremas/bandeiras das pedras, ou o veredito diferem do ensaio a seco')
    if not todas_op_:
        P.append('cunhagens_v405: as inscricoes de 30/10 a 01/11 tem de ser TODAS falas do operador (autor_de_cada_inscricao): nesta versao nao ha inscricao da gerencia')
    if not erratas_ok_:
        P.append('cunhagens_v405: as erratas E10 a E13 (assinadas pela gerencia c1, em nome proprio) ausentes ou diferentes do ensaio a seco')
    if not decisoes_ok_:
        P.append('cunhagens_v405: as decisoes D27 a D33 da gerencia ausentes ou diferentes do ensaio a seco')
    if not nomes_ok_:
        P.append('cunhagens_v405: os nomes das oito pedras ausentes')
    if not massa_ok_:
        P.append('cunhagens_v405: a leitura da v405 (os estatutos das leituras do operador) ausente ou diferente do ensaio a seco')
    if not reg404_ok_:
        P.append('cunhagens_v405: as pedras seladas da v404 deixaram de constar como registro (sha16 de ESPERADOS[pedras_v404_sha256])')
    if not kh_ok_:
        P.append('kh_n1_cobertura_v405 nao selou como o ensaio a seco (selo, veredito, nao move o gate)')
    # campos_fechados_e_leituras_v405: o que fechou (cada campo com os termos no kernel do rito) e o que entra (os dois postos e as leituras da cadeia da massa, lista que nao e' fechada, cada uma com o nome Lean); a MOLDURA (nenhuma frase proibida no registro; a frase certa)
    cf_ = core.get('campos_fechados_e_leituras_v405') or {}; xf_ = cf_.get('extras') or {}; ent_ = xf_.get('o_que_entra') or {}
    campos_ok_ = bool(set(xf_.get('o_que_fechou_campos') or {}) == set(DL_.CAMPOS_FECHADOS) and all(em_trio_(t_) for v_ in (xf_.get('o_que_fechou_campos') or {}).values() for t_ in v_.get('termos') or []))
    leit_ok_ = bool([l_.get('n') for l_ in ent_.get('leituras_da_cadeia_da_massa') or []] == list(range(1, len(ent_.get('leituras_da_cadeia_da_massa') or []) + 1)) and len(ent_.get('leituras_da_cadeia_da_massa') or []) >= 4 and ent_.get('lista_de_leituras_fechada') is False and all(str(l_.get('entra_como')).endswith(', nao teorema') and (l_.get('definicao_lean') is None or src_.get(l_.get('definicao_lean')) == l_.get('modulo')) for l_ in ent_.get('leituras_da_cadeia_da_massa') or []))
    postos_ok_ = bool([d_.get('estatuto') for d_ in ent_.get('dois_postos') or []] == ['POSTO', 'MEDIDA'] and all(src_.get(d_.get('definicao_lean')) == d_.get('modulo') for d_ in ent_.get('dois_postos') or []))
    import guarda_frases_v405 as GF_
    _txt_cf = json.dumps({k_: cf_.get(k_) for k_ in ('verdict', 'estatuto', 'limites', 'diz', 'nao_diz', 'erratas')}, ensure_ascii=False)
    moldura_ok_ = bool(xf_.get('a_frase_da_moldura') == DL_.FRASE_DA_MOLDURA_PT and DL_.ERRATA_E13 in (cf_.get('limites') or []) and not GF_.violacoes(_txt_cf) and all(not GF_.violacoes(json.dumps({k_: (core.get(n_) or {}).get(k_) for k_ in ('verdict', 'estatuto', 'scope', 'limites', 'diz', 'nao_diz')}, ensure_ascii=False)) for n_ in REG_FIXOS) and (GF_.controle_negativo() or {}).get('ok') is True)
    cf_ok_ = bool(cf_.get('all_verified') is True and cf_.get('does_not_gate_core') is True and cf_.get('verdict') == (ESP.get('registros_v405') or {}).get('campos_fechados_e_leituras_v405') and campos_ok_ and leit_ok_ and postos_ok_ and moldura_ok_ and not GUARDA.search(str(cf_.get('verdict') or '')))
    V['campos'] = {'ok': cf_ok_, 'verdict': cf_.get('verdict'), 'campos_ok': campos_ok_, 'leituras_ok': leit_ok_, 'postos_ok': postos_ok_, 'moldura_ok': moldura_ok_, 'n_campos': len(xf_.get('o_que_fechou_campos') or {}), 'n_leituras': len(ent_.get('leituras_da_cadeia_da_massa') or []), 'n_checks': len(cf_.get('checks') or [])}
    if not cf_ok_:
        P.append('campos_fechados_e_leituras_v405 nao selou inteiro (selo, veredito == o do ensaio, cada campo fechado com os termos no trio, as leituras da cadeia da massa e os dois postos com o nome Lean no modulo certo) ou a MOLDURA falhou (alguma frase proibida num registro novo, ou a frase certa ausente)')
    # ga_reclassificacao_v405 (por especificacao, AO LADO): a classe nova, as medidas em runtime iguais as do ensaio, a errata do parecer verbatim; o selado (a linha da tabela, a auditoria, o ga_window_status) identico
    ga_ = core.get(DL_.GA_REGISTRO) or {}; gm_ = ga_.get('mechanics') or {}; gv5_ = ga_.get('values') or {}; ge_ = ESP.get('ga_values') or {}
    lgm_ = [x_ for x_ in ((core.get('joint_coincidence_result_v3') or {}).get('inventory') or []) if isinstance(x_, dict) and x_.get('id') == 'ga_mass_window']
    ga_top_ = json.load(open(os.path.join(NOS, 'um_absoluto.json'), encoding='utf-8')).get('ga_window_status')
    ga_valores_ok_ = bool(ge_ and _feq({k_: gv5_.get(k_) for k_ in ge_}, ge_))
    ga_selado_ok_ = bool(len(lgm_) == 1 and lgm_[0].get('rule') == DL_.GA_CLASSE_ANTES and lgm_[0].get('admissible') is False and (core.get('ga_mass_audit') or {}).get('verdict') == (ESP.get('vereditos_v404') or {}).get('ga_mass_audit') and ga_top_ == ESP.get('ga_window_status'))
    ga_ok_ = bool(ga_.get('all_verified') is True and ga_.get('does_not_gate_core') is True and gm_.get('passed') is True and gm_.get('n_checks') == 6 and ga_.get('errata_do_parecer_ok') is True and ga_.get('verdict') == (ESP.get('registros_v405') or {}).get(DL_.GA_REGISTRO) and (ga_.get('extras') or {}).get('classe_agora') == DL_.GA_CLASSE_AGORA and ga_valores_ok_ and ga_selado_ok_ and not GUARDA.search(str(ga_.get('verdict') or '')))
    V['ga'] = {'ok': ga_ok_, 'verdict': ga_.get('verdict'), 'values': gv5_, 'valores_ok': ga_valores_ok_, 'selado_ok': ga_selado_ok_, 'classe_antes': DL_.GA_CLASSE_ANTES, 'classe_agora': DL_.GA_CLASSE_AGORA, 'n_checks': gm_.get('n_checks')}
    if not ga_ok_:
        P.append('ga_reclassificacao_v405 nao selou inteiro (selo, as seis medidas em runtime == as do ensaio, a errata do parecer verbatim, a classe nova) ou o selado mudou (a linha ga_mass_window, a auditoria da forma, o ga_window_status do JSON)')
    # gap_v405 (por especificacao, AO LADO): o lock, o gap, as medidas em runtime iguais as do ensaio, a medida negativa do fluxo
    gp_ = core.get(DL_.GAP_REGISTRO) or {}; gpm_ = gp_.get('mechanics') or {}; gpv_ = gp_.get('values') or {}; gpe_ = ESP.get('gap_values') or {}
    gp_valores_ok_ = bool(gpe_ and _feq({k_: gpv_.get(k_) for k_ in gpe_}, gpe_))
    gp_ok_ = bool(gp_.get('all_verified') is True and gp_.get('does_not_gate_core') is True and gpm_.get('passed') is True and gpm_.get('n_checks') == DL_.GAP_N_CHECKS and gp_.get('verdict') == (ESP.get('registros_v405') or {}).get(DL_.GAP_REGISTRO) and gp_valores_ok_ and not GUARDA.search(str(gp_.get('verdict') or '')))
    V['gap'] = {'ok': gp_ok_, 'verdict': gp_.get('verdict'), 'values': gpv_, 'valores_ok': gp_valores_ok_, 'n_checks': gpm_.get('n_checks')}
    if not gp_ok_:
        P.append('gap_v405 nao selou inteiro (selo, as medidas em runtime == as do ensaio, a medida negativa do fluxo)')
    # os registros por spec da v404 (cunhagens_v404 e kh_n1_cobertura_v404, RECRIADOS): iguais aos selados
    c4_ = core.get('cunhagens_v404') or {}; k4_ = core.get('kh_n1_cobertura_v404') or {}; c4b_ = _base_core(PK).get('cunhagens_v404') or {}
    c4_ok_ = bool(c4_.get('all_verified') is True and c4_.get('does_not_gate_core') is True and bool(c4b_) and _feq(c4_.get('verbatim'), c4b_.get('verbatim')) and _feq(c4_.get('extras'), c4b_.get('extras')) and _feq(c4_.get('erratas'), c4b_.get('erratas')) and c4_.get('verdict') == (ESP.get('registros_v404') or {}).get('cunhagens_v404') and not GUARDA.search(str(c4_.get('verdict') or '')))
    k4_ok_ = bool(k4_.get('all_verified') is True and k4_.get('does_not_gate_core') is True and k4_.get('verdict') == (ESP.get('registros_v404') or {}).get('kh_n1_cobertura_v404'))
    V['cunh404b'] = {'n': len(c4_.get('verbatim') or {}), 'ok': c4_ok_, 'verdict': c4_.get('verdict'), 'kh_ok': k4_ok_}
    if not c4_ok_:
        P.append('cunhagens_v404 (recriada pelo rito) nao confere como a v404 a selou (selo, veredito, as falas, as erratas E7 a E9 e os extras)')
    if not k4_ok_:
        P.append('kh_n1_cobertura_v404 (recriada pelo rito) nao selou como a v404 a selou (selo, veredito, nao move o gate)')
'''


# as regras dos demais scripts do pos-rito (chain, fechar, harnesses, mapa, superficies): em arquivo proprio, escrito pela ferramenta Write (barras invertidas e apostrofos nao passam pelo heredoc do Bash)
exec(compile(open(os.path.join(HERE, "adaptar_regras2_v405.py"), encoding="utf-8").read(), "adaptar_regras2_v405.py", "exec"))

def main():
    alvos = sys.argv[1:] or list(ARQS)
    for nome in alvos:
        p = os.path.join(HERE, nome); sem = p + ".semente_lote_F"
        if not os.path.exists(sem):
            shutil.copyfile(p, sem)
        txt = open(sem, "rb").read().decode("utf-8")
        atual = open(p, "rb").read()
        x = T(txt, nome); ARQS[nome](x)
        if nome.endswith(".py"):
            ast.parse(x.t)
        novo = x.t.encode("utf-8")
        if novo == atual:
            print("igual", nome); continue
        open(p + ".bak_" + TS, "wb").write(atual)
        open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo); os.replace(p + ".tmp", p)
        print("adaptado", nome, len(novo))


if __name__ == "__main__":
    main()
