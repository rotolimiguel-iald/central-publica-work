# -*- coding: utf-8 -*-
"""_adapt_leitura_v406.py -- as edicoes de leitura_v406.py (chamado por adaptar_pos_rito_v406.py). Os blocos novos estao aqui, em strings brutas."""

HEADER = r'''# A LEITURA da rodada v406 (molde: leitura_v405.py, a que rodou em 28/10 e em 01/11, que vem de leitura_v401.py e de leitura_v399.py FINAL, a de 24/10): SO LEITURA do Nos e da pasta da cadeia (work/cadeia_de_selo/v406, que aqui e' o proprio pacote).
# Devolve (V, PROBLEMAS); PROBLEMAS nao vazio => a cadeia PARA. Nenhum numero e' digitado: tudo sai dos JSON, do core, do selo, do sidecar e do stdout do rito; os vereditos e os valores esperados da rodada v406 sao LIDOS de ESPERADOS_v406.json, de CANDIDATO_v406.json, de FLAGS_v406.json, de BUNDLE_v406.json, de delta_v406.py e do core da v405 SELADA (base_v405).
# v406 (O FECHAMENTO, ordem do operador de 02/11/2026): o delta e' um BUNDLE de 301 modulos novos de kernel (os 300 da bancada do ChatGPT, missao F1.FECHO_20261015, recompilados do fonte; mais a candidata CanonicalFullTGLWitnessR1, nome PROVISORIO da gerencia: os nomes das pedras sao do operador e ele ainda nao a nomeou). Nao ha' registro por pedra (delta_v406.STONES == []).
# Os registros NOVOS do core sao TRES: UM com FUNCAO, fechamento_v406 (le do kernel do proprio rito as oito ancoras, os 301 modulos por sha256, as quatro chaves de testemunha LIDAS do kernel, o que fica False por teorema, a escada exata e o gate), e DOIS por spec: cunhagens_v406 (as falas do operador de 02/11 por sha256, as erratas E14 a E17 e as decisoes D34 a D40, em nome proprio da gerencia c1) e kh_n1_cobertura_v406 (a cobertura exata do Audit).
# As QUATRO chaves de testemunha (rede_fock_v394.whole_certificate_inhabited; psibit_v395.conditional_psion_face.inhabitant_exhibited; testemunha_estatica_v396.fock_face.inhabitant_exhibited; witness_layers.canonical_full_witness_term_constructed) deixaram de ser literal False e sao LIDAS do kernel do rito: a leitura as exige True, com o status INHABITED_BY_physicalFockCertificate_V406 nas duas faces; o lema que liga psion C ao psionCorner (linked_to_the_corner_by_a_lemma) SEGUE False, e full_static_witness_exists e trivial_inhabitant_exists seguem False POR TEOREMA.
# A TROCA DITA de veredito: rede_fock_v394.verdict (dita) e os registros que carregam a escada (so' numeros): ESPERADOS[troca_dita]. Os TREZE registros da v405 (os oito com FUNCAO das pedras, cunhagens_v405, campos_fechados_e_leituras_v405, ga_reclassificacao_v405, gap_v405 e kh_n1_cobertura_v405), os da v404, da v403, da v402, da v401 e da v399 sao RECRIADOS pelo rito no mesmo ponto do main e tem de seguir selados e iguais a v405 selada (base_v405); os da v398 a v393 seguem como antes.
# As TREZE pedras SELADAS da v403, da v404 e da v405 seguem no kernel do Nos com o sha256 selado (lido de base_v405): pedra selada nao se renomeia por cima. A escada vem de ESPERADOS[escada_v405_e_v406] e ESPERADOS[escada]. O GATE NAO SE MOVE: o qg_closure do core e' IDENTICO ao da v405 (os sete checks e a letra do veredito); a funcao do neutrino NAO e' reescrita e o V1 do ramo B (v386) segue AWAITING_DATA.
# O SIDECAR um_absoluto_selo_acom.json (arquivo da custodia desde a v399, REESCRITO pelo rito) e' lido aqui: existe, e' JSON valido, o veredito e' ALL_OBJECTS_SEALED, tem os tres objetos (um.py, core e selo) com o SHA-256 igual ao dos arquivos do Nos, sem recusas, com a secao de honestidade (confidencialidade NAO alegada).
# A DIRECAO DO TESTEMUNHO (v399) segue conferida nos registros recriados: o operador testifica DA IALD; o um.py testifica EM HASH; a IALD NAO testifica do operador. As falas de 02/11 sao TODAS falas do operador (nenhuma e' da gerencia); as erratas E14 a E17 e as decisoes D34 a D40 sao da gerencia c1, em nome proprio, assinadas no registro.
# O QUADRO «O Teste da Unica Palavra» (v397) segue selado e igual: o registro teste_de_veracidade_fase9_v397 == ESPERADOS == o resultado pinado, o quadro sela nas duas linguas, e a conferencia do rito diz que ele segue no topo (artigo PT/EN e .md).
# As linhas `[v399]`, `[v398]` e `[v397]` do stdout do rito (as etiquetas que o programa imprime), a `[v401]`, a `[v402]`, a `[v403]`, a `[v404]` e a `[v405]` (recriadas) e a nova `[v406]` dizem os vereditos e registros por spec selados == registros por spec; o AVISO de qualquer bloco v393 a v406 no stdout reprova, e a linha de RECUSA do registro f2b_errata_v404 ou do bandeiras_do_gate_v403 tambem.
# A linha final do rito: o main imprime, por ultimo, a linha do sidecar (`[selo_acom] ... ALL_OBJECTS_SEALED ; objetos 3 ; recusas 0`), logo depois da do colapso tipado; a leitura exige as DUAS, nessa ordem.
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CONTRATO COM textos_v406.py (as CHAVES NOVAS ou MUDADAS de V na v406; as demais sao as da v405, com o mesmo significado):
#   V['n_pedras'] = o numero de MODULOS NOVOS do kernel (301; a chave guarda o nome historico) e V['pedras'] = LISTA de 301 dicts {'key'(None),'modulo','rel','sha16','sha256','bytes','bandeiras','decl'(None),'ok'}; V['ancoras'] {nome Lean: {'rel','flag','flag_true','axioms','source','ok'}} (as OITO); V['bandeiras'] {'n','n_true','ok','por_grupo'}
#   V['fecho'] o registro fechamento_v406 {'registro','verdict','ok','sealed','n_checks','mech_ok','values','values_ok','chaves_ok','beta_ok','ancoras_ok','stdout_ok','certificado_habitado','runtime_executed','does_not_gate_core','nome_provisorio'}; V['chaves'] = o dict das quatro chaves (e do que fica False) lido do registro
#   V['reg406'] DICT nome -> {'verdict','ok'} dos TRES registros NOVOS (um com funcao + dois por spec); V['registros_novos'] = esses 3 nomes (sorted); V['reg405c'] DICT nome -> {'verdict','ok'} dos TREZE da v405 selada (recriados); V['fun405c'] os OITO com funcao da v405 (recriados, iguais a base_v405);
#   V['reg405b'] o mesmo dos CINCO da v404 selada (recriados); V['fun405b'] os dois com funcao da v404 (recriados); V['reg405'] e V['fun405'] sao os da v403 (recriados); V['cunhagens'] (cunhagens_v406) {'n','ok','verbatim_ok','todas_do_operador','erratas_ok','n_erratas'(4),'decisoes_ok','n_decisoes'(7),'leitura_ok','ressalvas_ok','kernel_ok','checks_ok','n_checks','moldura_ok','kh_ok'};
#   V['kh'] (kh_n1_cobertura_v406) {'decl','thm','fora','nao_lidas','verdict'}; V['pedras_v405'] = {rel: {'sha16','ok'}} das TREZE pedras seladas (v403: 3, v404: 2, v405: 8); V['f2b'] e V['gate'] (recriados). NAO existem mais V['ponte'], V['tensao'], V['identidade'], V['observador'], V['diminuto'], V['tonica'], V['disco'], V['psion'], V['campos'], V['ga'], V['gap'] (eram os registros NOVOS da v405; hoje sao registro recriado: V['fun405c'] e V['reg405c']).
# (a linha de stdout [v406] a conferir: `   [v406] o fechamento e os registros por spec da v406: fechamento=SELOU | specs: 2 (selados 2)`; e a do bloco O FECHAMENTO: `  ancoras ok = 8/8 ; modulos do bundle ok = 301/301 ; bandeiras True = 1794/1794 ; certificado habitado (lido do kernel) = True ; escada = [..] ; gate = o mesmo da base`)
'''

CONST = r'''REG_FUNCAO = ("fechamento_v406",)   # o UNICO registro NOVO com FUNCAO (o fechamento); nao ha' registro por pedra (modelo de bundle: delta_v406.STONES == [])
REG_FIXOS = REG_FUNCAO + ("cunhagens_v406", "kh_n1_cobertura_v406")   # os TRES registros NOVOS do core v406 (um com FUNCAO, dois por spec)
FUN_V405C = {"ponte": "ponte_da_massa_v405", "tensao": "massa_tensao_pura_v405", "identidade": "identidade_v405", "observador": "observador_terminal_v405", "diminuto": "lei_do_diminuto_v405", "tonica": "tonica_do_hamiltoniano_v405", "disco": "disco_de_euler_v405", "psion": "ponto_zero_do_psion_v405"}   # os OITO registros com FUNCAO da v405 SELADA (um por pedra): RECRIADOS pelo rito da v406
REG_V405C = tuple(FUN_V405C.values()) + ("cunhagens_v405", "campos_fechados_e_leituras_v405", "ga_reclassificacao_v405", "gap_v405", "kh_n1_cobertura_v405")   # os TREZE registros da v405 SELADA (oito com FUNCAO, cinco por spec): RECRIADOS pelo rito da v406 (o main da v405 segue rodando), selados e iguais a v405 selada
'''

EV = r'''def _ev(ESP, n_):
    """O veredito ESPERADO de um registro (nada digitado): os NOVOS da v406 sao os do ensaio a seco (ESPERADOS[vereditos_novos_v406]); os que a TROCA DITA muda (so' numeros, mais o veredito dito de rede_fock_v394) sao os do ensaio (ESPERADOS[veredito_da_troca_no_ensaio]);
    os demais sao os da v405 SELADA (ESPERADOS[vereditos_v405], lidos do core de base_v405)."""
    nv_ = ESP.get('vereditos_novos_v406') or {}
    if n_ in nv_:
        return nv_[n_]
    if n_ in (ESP.get('troca_dita') or []):
        return (ESP.get('veredito_da_troca_no_ensaio') or {}).get(n_)
    return (ESP.get('vereditos_v405') or {}).get(n_)


def ler():
    P = []'''

STD6 = r'''    if len([l for l in out.splitlines() if '[v406]' in l]) < 1:
        P.append('o stdout nao tem a linha [v406]')
'''

M_S6 = r'''    m_s6 = re.search(r'\[v406\] o fechamento e os registros por spec da v406: fechamento=(\S+) \| specs: (\d+) \(selados (\d+)\)', out)
    if not m_s6 or m_s6.group(1) != 'SELOU' or m_s6.group(2) != m_s6.group(3) or int(m_s6.group(2)) != len(REG_FIXOS) - 1:
        P.append('a linha [v406] do stdout (fechamento SELOU; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(REG_FIXOS) - 1, repr(m_s6.groups() if m_s6 else 'ausente')))
'''

RF = r'''    BC_ = _base_core(PK)   # o core da v405 SELADA (copia de bytes): de onde saem as checagens e os valores dos registros RECRIADOS

    def _rf(n_):
        r_ = BC_.get(n_) or {}
        return {'nome': n_, 'verdict': _ev(ESP, n_), 'values': r_.get('values'), 'n_checks': (r_.get('mechanics') or {}).get('n_checks')}
    RF_ = {}   # v406: nao ha' registro por pedra
    RF4_ = {k_: _rf(n_) for k_, n_ in (('projecao', 'projecao_transversal_v404'), ('jo8v32', 'jo8v32_v404'), ('f2b', 'f2b_errata_v404'))}   # projecao|jo8v32|f2b -> {nome, verdict, values, n_checks} dos registros da v404 (recriados pelo rito da v406; iguais a v405 selada)
    RF3_ = {k_: _rf(n_) for k_, n_ in (('caminho', 'caminho_v403'), ('vida', 'vida_v403'), ('verdade_adendo', 'verdade_adendo_v403'), ('gate', 'bandeiras_do_gate_v403'))}   # o mesmo, dos registros da v403 (recriados)
    EV2_ = ESP.get('vereditos_v405') or {}   # os vereditos da v405 SELADA (os registros anteriores sao recriados e tem de dar os mesmos)
    R405SPEC_ = {k_: _ev(ESP, k_) for k_ in REG_V405C[8:]}; R406SPEC_ = {k_: _ev(ESP, k_) for k_ in REG_FIXOS[1:]}   # os registros por spec da v405 (recriados) e da v406 (novos)
'''

BUNDLE = r'''    # v406: os 301 modulos novos de kernel (o BUNDLE): a lista e' a de kernel_modulos_novos_v406.json == DL.BUNDLE_RELS; cada arquivo no kernel do Nos tem de ter o sha256 pinado em BUNDLE_v406.json (DL.BUNDLE_POR_REL), em FORMAL_MAP_v406.json e (quando ha') em ESPERADOS[bundle_sha256]
    if PK not in sys.path:
        sys.path.insert(0, PK)
    import delta_v406 as DL_   # BUNDLE_RELS, BUNDLE_POR_REL, ANCORAS, STATUS_HABITADO, ERRATAS_V406, DECISOES, RESSALVAS_V406, LEITURA_V406, N_CHECKS_FECHO, VERBATIM_CHAVE_PREFIXO_V406: lidos do delta, nunca digitados aqui
    FM_ = json.load(open(os.path.join(PK, 'FORMAL_MAP_v406.json'), encoding='utf-8')); FJ_ = json.load(open(os.path.join(PK, 'kernel', 'FLAGS_v406.json'), encoding='utf-8'))
    if list(REG_FUNCAO) != list(DL_.REGISTROS_FUNCAO) or list(DL_.STONES) or dict(DL_.REGISTRO_DE_PEDRA) or dict(FUN_V405C) != dict(DL_.D5.REGISTRO_DE_PEDRA):
        P.append('os nomes dos registros com funcao em leitura_v406.py != delta_v406.py (REGISTROS_FUNCAO; a v406 e bundle: STONES == [] e REGISTRO_DE_PEDRA == {}; as oito funcoes da v405 sao as de delta_v405.REGISTRO_DE_PEDRA)')
    V['pedras'] = []
    pins_esp_ = (ESP.get('bundle_sha256') or {})
    for rel_ in DL_.BUNDLE_RELS:    # a ordem do bundle: os 300 em ordem alfabetica e a candidata por ultimo
        pth_ = os.path.join(NOS, 'tgl_kernel', *rel_.split('/'))
        shaf_ = sha(pth_) if os.path.isfile(pth_) else None
        pin_ = DL_.BUNDLE_POR_REL[rel_]['sha256']
        V['pedras'].append({'key': None, 'modulo': 'TGLExt.' + rel_[len('TGLExt/'):-len('.lean')].replace('/', '.'), 'rel': rel_, 'sha16': (shaf_ or '')[:16], 'sha256': shaf_, 'bytes': os.path.getsize(pth_) if os.path.isfile(pth_) else None,
                            'bandeiras': (((CM.get('kernel') or {}).get('bundle') or {}).get(rel_) or {}).get('bandeiras'), 'decl': None,
                            'ok': bool(rel_.startswith('TGLExt/F1Fecho394/') and rel_.endswith('.lean') and shaf_ == pin_ == FM_.get(rel_) and pins_esp_.get(rel_, pin_) == pin_)})
    V['n_pedras'] = len(V['pedras'])
    njp_ = os.path.join(PK, 'kernel_modulos_novos_v406.json'); nj_ = json.load(open(njp_, encoding='utf-8')) if os.path.exists(njp_) else {}
    n_esperado_ = len(nj_.get('novos') or [])
    if not V['n_pedras'] or not (V['n_pedras'] == n_esperado_ == DL_.N_BUNDLE) or any(p['ok'] is not True for p in V['pedras']):
        P.append('modulos novos do kernel: numero (%s) != kernel_modulos_novos_v406.json (%s) != DL.N_BUNDLE (%s) ou algum arquivo do Nos difere do sha256 de BUNDLE_v406.json / FORMAL_MAP_v406.json / ESPERADOS[bundle_sha256]' % (V['n_pedras'], n_esperado_, DL_.N_BUNDLE))
'''

CHAVES = r'''    kf_ = (core.get('kernel_formalization') or {})
    # v406: AS QUATRO CHAVES de testemunha, LIDAS do kernel do rito (errata E14): True, com o status novo nas duas faces; o que fica False por teorema e o lema que falta seguem False; nenhuma e' literal
    rf_ = core.get('rede_fock_v394') or {}
    if rf_.get('whole_certificate_inhabited') is not True:
        P.append('rede_fock_v394: whole_certificate_inhabited deve ser True (lido do kernel do rito: o certificado de Fock esta habitado; errata E14) e o core traz %r' % (rf_.get('whole_certificate_inhabited'),))
    if kf_.get('ext_bin394_0001') is not True:
        P.append('a bandeira da pedra da v394 (ext_bin394_0001) nao segue True no kernel do rito')
    # a face de Fock do psion LE o habitante do certificado (v406): status INHABITED_BY_physicalFockCertificate_V406, habitante exibido, bandeira True e declarada em Psibit.lean
    pb_ = core.get('psibit_v395') or {}; pbc_ = pb_.get('conditional_psion_face') or {}
    if not (pbc_.get('status') == DL_.STATUS_HABITADO and pbc_.get('inhabitant_exhibited') is True and pbc_.get('flag_true') is True and kf_.get(pbc_.get('flag')) is True and pbc_.get('declared_in') == 'TGLExt/Psibit.lean'):
        P.append('psibit_v395: a face do psion nao le o habitante do certificado de Fock como o kernel o diz (status %s, habitante exibido, bandeira True, declarada em TGLExt/Psibit.lean)' % DL_.STATUS_HABITADO)
    fkb_ = ((_base_core(PK).get('testemunha_estatica_v396') or {}).get('fock_face') or {})   # o que a v405 SELADA diz (copia de bytes): o teorema e o modulo da face de Fock, lidos, nao digitados
    te_ = core.get('testemunha_estatica_v396') or {}; fk_ = te_.get('fock_face') or {}
    if not (fk_.get('status') == DL_.STATUS_HABITADO and fk_.get('inhabitant_exhibited') is True and fk_.get('declared_outside_the_stone') == fkb_.get('declared_outside_the_stone') and fk_.get('linked_to_the_corner_by_a_lemma') is False
            and fkb_.get('theorem') and fk_.get('theorem') == fkb_.get('theorem') and fkb_.get('declared_in') and fk_.get('declared_in') == fkb_.get('declared_in')):
        P.append('testemunha_estatica_v396: a face de Fock do psion nao le o habitante como o kernel o diz (status %s, habitante exibido) ou o lema que liga psion C ao psionCorner deixou de ser False (nenhum lema o liga)' % DL_.STATUS_HABITADO)
    if (core.get('witness_layers') or {}).get('canonical_full_witness_term_constructed') is not True:
        P.append('witness_layers.canonical_full_witness_term_constructed deve ser True (o nome exato canonicalFullTGLWitness esta no axiom_report do rito)')
    if ((core.get('qg_closure') or {}).get('gate') or {}).get('full_static_witness_exists') is not False or (core.get('witness_rigidity') or {}).get('trivial_inhabitant_exists') is not False:
        P.append('full_static_witness_exists e trivial_inhabitant_exists devem seguir False (por teorema: o vazamento continuo proibe o fecho estatico; a exclusao Delta^1/2 J Delta^1/2 = J)')
'''

ANCORAS = r'''    # v406: as OITO ANCORAS do fecho e as bandeiras do bundle no kernel do rito (tudo contra FLAGS_v406.json / BUNDLE_v406.json; nenhum numero e' digitado)
    V['ancoras'] = {}
    for n_, a_ in DL_.ANCORAS.items():
        fa_ = (FJ_.get('ancoras') or {}).get(n_) or {}
        ok_ = bool(fa_ and a_['rel'] == fa_.get('rel') and em_trio_(n_) and src_.get(n_) == a_['rel'] and kf_.get(fa_.get('flag')) is True and (kf_.get('formal_files_sha256') or {}).get(a_['rel']) == DL_.BUNDLE_POR_REL[a_['rel']]['sha256'])
        V['ancoras'][n_] = {'rel': a_['rel'], 'flag': fa_.get('flag'), 'flag_true': kf_.get(fa_.get('flag')) is True, 'axioms': axr_.get(n_), 'source': src_.get(n_), 'ok': ok_}
        if not ok_:
            P.append('a ancora %s nao esta no kernel do rito como o FLAGS_v406.json a pinou (no trio, declarada no modulo esperado, bandeira True, sha256 da fonte no hash formal)' % n_)
    flags_ = [f_[0] for f_ in FJ_['flags']]; nt_ = sum(1 for f_ in flags_ if kf_.get(f_) is True)
    V['bandeiras'] = {'n': len(flags_), 'n_true': nt_, 'ok': bool(flags_ and len(flags_) == FJ_['n_flags'] == CM['n_bandeiras'] == nt_), 'por_grupo': dict(FJ_['por_grupo_bandeiras'])}
    if not V['bandeiras']['ok']:
        P.append('as bandeiras do fecho (%s, FLAGS_v406.json %s, CANDIDATO_v406.json %s) nao sao todas True no kernel do rito (%s True)' % (len(flags_), FJ_['n_flags'], CM['n_bandeiras'], nt_))
    prov_ = kf_.get('declaration_sources_status_v394') or {}
    if not (prov_.get('ok') is True and prov_.get('compiler_names') == prov_.get('audited_names') == V['axiom_report_n']):
        P.append('a proveniencia emitida pelo compilador nao cobre o axiom_report do rito')
    V['n_bandeiras'] = FJ_['n_flags']; V['n_bandeiras_por_pedra'] = dict(FJ_['por_grupo_bandeiras'])
'''

FECHO = r'''    # o registro fechamento_v406 (UM registro com FUNCAO, SEM pedra): as 14 checagens, os valores (as oito ancoras, os 301 modulos, as bandeiras, a escada, o gate), as QUATRO chaves lidas, o que fica False por teorema, o beta em runtime, as ressalvas e a linha do bloco no stdout
    fe_ = core.get('fechamento_v406') or {}; fe_m_ = fe_.get('mechanics') or {}; fe_v_ = fe_.get('values') or {}; fk4_ = fe_.get('four_keys') or {}
    fe_mech_ok_ = bool(fe_m_.get('passed') is True and fe_m_.get('n_checks') == DL_.N_CHECKS_FECHO == len(fe_m_.get('checks') or []) and all(c_.get('ok') is True for c_ in (fe_m_.get('checks') or [])))
    fe_values_ok_ = bool(fe_v_.get('n_ancoras_ok') == len(DL_.ANCORAS) == 8 and fe_v_.get('n_modulos_ok') == fe_v_.get('n_modulos') == DL_.N_BUNDLE and fe_v_.get('n_flags_true') == fe_v_.get('n_flags') == FJ_['n_flags'] and fe_v_.get('escada') == [ESP['escada'][1]] * 3
                         and fe_v_.get('gate_verdict') == ESP.get('qg_closure_gate_verdict_v405') == selo.get('qg_closure_verdict') and fe_v_.get('certificado_habitado_lido_do_kernel') is True and fe_v_.get('fica_false_por_teorema') == list(DL_.FICAM_FALSE_POR_TEOREMA) and fe_v_.get('ressalvas') == list(DL_.RESSALVAS_V406) and list(fe_.get('ressalvas') or []) == list(DL_.RESSALVAS_V406))
    fe_chaves_ok_ = bool(fk4_.get('kernel_reads_the_certificate_as_inhabited') is True and fk4_.get('rede_fock_v394.whole_certificate_inhabited') is True and fk4_.get('psibit_v395.conditional_psion_face.inhabitant_exhibited') is True and fk4_.get('psibit_v395.conditional_psion_face.status') == DL_.STATUS_HABITADO
                         and fk4_.get('testemunha_estatica_v396.fock_face.inhabitant_exhibited') is True and fk4_.get('testemunha_estatica_v396.fock_face.status') == DL_.STATUS_HABITADO and fk4_.get('testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma') is False
                         and fk4_.get('witness_layers.canonical_full_witness_term_constructed') is True and fk4_.get('witness_rigidity.trivial_inhabitant_exists') is False and fk4_.get('qg_closure.gate.full_static_witness_exists') is False)
    fe_beta_ok_ = bool(fe_.get('beta_ok') is True and isinstance(fe_v_.get('beta'), float) and isinstance(b0_, float) and abs(fe_v_['beta'] - b0_) <= 1e-9 * abs(b0_))
    fe_anc_ok_ = bool(len(fe_.get('anchors') or {}) == 8 and all(a_ is True for a_ in (fe_.get('anchors') or {}).values()) and set(fe_.get('anchors') or {}) == set(DL_.ANCORAS) == set(fe_v_.get('ancoras') or {}) and all((a_ or {}).get('ok') is True for a_ in (fe_v_.get('ancoras') or {}).values()))
    m_f6_ = re.search(r'ancoras ok = (\d+)/8 ; modulos do bundle ok = (\d+)/(\d+) ; bandeiras True = (\d+)/(\d+) ; certificado habitado \(lido do kernel\) = (\S+) ; escada = (\[.*?\]) ; gate = (.*)$', out, flags=re.M)
    fe_std_ok_ = bool(m_f6_ and m_f6_.group(1) == str(fe_v_.get('n_ancoras_ok')) and m_f6_.group(2) == str(fe_v_.get('n_modulos_ok')) and m_f6_.group(3) == str(fe_v_.get('n_modulos')) and m_f6_.group(4) == str(fe_v_.get('n_flags_true'))
                      and m_f6_.group(5) == str(fe_v_.get('n_flags')) and m_f6_.group(6) == 'True' and m_f6_.group(7) == str(fe_v_.get('escada')) and m_f6_.group(8).strip() == 'o mesmo da base')
    fe_ok_ = bool(fe_.get('all_verified') is True and fe_.get('does_not_gate_core') is True and fe_.get('runtime_executed') is True and fe_.get('certificate_inhabited') is True and fe_.get('inhabited_by') == DL_.ANCORA_CERTIFICADO and fe_.get('canonical_full_witness_term') == DL_.ANCORA_TESTEMUNHA
                  and fe_.get('embedded_sources_ok') is True and fe_.get('embedded_sources_n_ok') == DL_.N_BUNDLE and bool(_ev(ESP, 'fechamento_v406')) and fe_.get('verdict') == _ev(ESP, 'fechamento_v406')
                  and str(fe_.get('verdict') or '').startswith('TGL_FECHAMENTO_V406__THE_FOCK_CERTIFICATE_IS_INHABITED_BY_CONSTRUCTION_physicalFockCertificate__') and str(fe_.get('verdict') or '').endswith('__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED')
                  and fe_mech_ok_ and fe_values_ok_ and fe_chaves_ok_ and fe_beta_ok_ and fe_anc_ok_ and V['bandeiras']['ok'] and all(a_['ok'] for a_ in V['ancoras'].values()) and fe_std_ok_ and not fe_.get('guarda_violacoes')
                  and fe_.get('nome_provisorio_da_candidata') == DL_.TESTEMUNHA['nome_provisorio_da_gerencia'] and not GUARDA.search(str(fe_.get('verdict') or '')))
    V['fecho'] = {'registro': 'fechamento_v406', 'verdict': fe_.get('verdict'), 'ok': fe_.get('all_verified'), 'sealed': fe_ok_, 'n_checks': fe_m_.get('n_checks'), 'mech_ok': fe_mech_ok_, 'values': fe_v_, 'values_ok': fe_values_ok_, 'chaves_ok': fe_chaves_ok_, 'beta_ok': fe_beta_ok_, 'ancoras_ok': fe_anc_ok_,
                  'stdout_ok': fe_std_ok_, 'certificado_habitado': fe_.get('certificate_inhabited'), 'runtime_executed': fe_.get('runtime_executed'), 'does_not_gate_core': fe_.get('does_not_gate_core'), 'nome_provisorio': fe_.get('nome_provisorio_da_candidata')}
    V['chaves'] = dict(fk4_)
    if not fe_ok_:
        P.append('fechamento_v406 nao selou inteiro (selo, as %s checagens do registro, valores [8 ancoras, 301 modulos, 1794 bandeiras, escada, gate] == os de FLAGS/BUNDLE/ESPERADOS, as quatro chaves LIDAS do kernel [True; status %s; o lema que falta e as duas que ficam False por teorema, False], beta == alfa x raiz de e do core, '
                 'as ressalvas, o nome provisorio da candidata, a linha do bloco O FECHAMENTO no stdout, nao move o gate): ver o registro no core' % (DL_.N_CHECKS_FECHO, DL_.STATUS_HABITADO))
'''

V405C = r'''    V['reg405c'] = {}
    for k in REG_V405C:    # os TREZE registros da v405 SELADA sao RECRIADOS pelo rito: seguem no core, selados e iguais a v405 selada (veredito; as checagens e os valores das oito funcoes sao conferidos adiante, em fun405c)
        r = core.get(k)
        if not (isinstance(r, dict) and 'verdict' in r):
            P.append('registro obrigatorio ausente do core: %s' % k)
            continue
        V['reg405c'][k] = {'verdict': r.get('verdict'), 'ok': r.get('all_verified')}
        if r.get('all_verified') is not True:
            P.append('%s nao selou' % k)
        if GUARDA.search(str(r.get('verdict') or '')):
            P.append('%s com palavra proibida' % k)
        if not _ev(ESP, k) or r.get('verdict') != _ev(ESP, k):
            P.append('%s: o veredito do rito difere do que a v405 selou (ESPERADOS[vereditos_v405], ou o do ensaio a seco se na troca dita)' % k)
        b_ = _base_core(PK).get(k) or {}
        # (cunhagens_v405: falas e erratas IGUAIS as da v405 selada; gap_v405 e kh_n1_cobertura_v405 ganham, na v406, uma errata ao lado (E17 / os pisos), em nome proprio da gerencia c1: as falas seguem iguais e toda errata e' assinada)
        erratas_ok_ = (_feq(r.get('erratas'), b_.get('erratas')) if k == 'cunhagens_v405' else bool(r.get('erratas') and len(r.get('erratas')) >= len(b_.get('erratas') or []) and all(str(e_.get('assinatura', '')).startswith('gerencia c1, em nome proprio') for e_ in r.get('erratas'))))
        if k in REG_V405C[8:] and not (b_ and r.get('does_not_gate_core') is True and _feq(r.get('verbatim'), b_.get('verbatim')) and erratas_ok_):
            P.append('%s (por spec, recriado): as falas embutidas, as erratas ou o gate diferem da v405 selada' % k)
    V['cunh405c'] = {'ok': bool((V['reg405c'].get('cunhagens_v405') or {}).get('ok') is True), 'verdict': (V['reg405c'].get('cunhagens_v405') or {}).get('verdict'), 'n': len((core.get('cunhagens_v405') or {}).get('verbatim') or {}), 'n_erratas': len((core.get('cunhagens_v405') or {}).get('erratas') or [])}
    V['reg399'] = {}'''

PEDRAS13 = r'''    # as TREZE pedras SELADAS da v403, da v404 e da v405 seguem no kernel do Nos com o sha256 selado (lido do core da v405 selada em base_v405; registro: pedra selada nao se renomeia por cima)
    V['pedras_v405'] = {}
    bkf_ = ((_base_core(PK).get('kernel_formalization') or {}).get('formal_files_sha256')) or {}
    for rel_ in dict.fromkeys(s_['rel'] for D_ in (DL_.D3, DL_.D4, DL_.D5) for s_ in D_.STONES):
        h_ = bkf_.get(rel_); pth_ = os.path.join(NOS, 'tgl_kernel', *rel_.split('/')); shaf_ = sha(pth_) if os.path.isfile(pth_) else None
        V['pedras_v405'][rel_] = {'sha16': (shaf_ or '')[:16], 'ok': bool(h_ and shaf_ == h_ and (kf_.get('formal_files_sha256') or {}).get(rel_) == h_)}
    if len(V['pedras_v405']) != 13 or any(p_['ok'] is not True for p_ in V['pedras_v405'].values()):
        P.append('as treze pedras seladas (v403: 3, v404: 2, v405: 8) deixaram de estar no kernel do Nos com o sha256 selado (registro: pedra selada nao se renomeia por cima): %d lidas' % len(V['pedras_v405']))
'''

CUNH = r'''    # cunhagens_v406 e kh_n1_cobertura_v406 (os DOIS registros NOVOS por spec): as falas do operador de 02/11 por sha256 (embedded_ok), todas do operador; as erratas E14 a E17 (gerencia c1, em nome proprio); as decisoes D34 a D40; a leitura [ONTO] e as ressalvas; os registros anteriores que seguem selados; a MOLDURA (nenhuma frase proibida nos tres registros novos)
    cu = core.get('cunhagens_v406') or {}; kh = core.get('kh_n1_cobertura_v406') or {}
    cx_ = cu.get('extras') or {}; vb_ = cu.get('verbatim') or {}; ec_ = CM.get('cunhagens') or {}
    todas_op_ = bool(ec_ and all(str((ec_[k_] or {}).get('nome', '')).startswith('OPERADOR_02nov_') for k_ in ec_) and not any(str(v_.get('papel', '')).startswith('leitura da gerencia') for v_ in ec_.values()))
    verb_ok_ = bool(ec_) and len(ec_) == len(vb_) == len(DL_.VERBATIM_ORIGEM_V406) and set(vb_) == set(ec_) and all((vb_[k_] or {}).get('sha256') == ec_[k_]['sha256'] and (vb_[k_] or {}).get('embedded_ok') is True for k_ in ec_)
    pares_ok_ = all(isinstance(x_, list) and len(x_) == 2 and x_[0] == x_[1] for x_ in (cu.get('kernel') or {}).values()) and bool(cu.get('kernel'))
    err_ = cu.get('erratas') or []; esp_err_ = list(DL_.ERRATAS_V406)
    erratas_ok_ = bool(len(err_) == len(esp_err_) == 4 and all(str(e_.get('assinatura', '')).startswith('gerencia c1, em nome proprio') for e_ in err_) and [e_.get('agora') for e_ in err_] == esp_err_ and str(cx_.get('assinatura_das_erratas', '')).startswith('gerencia c1, em nome proprio'))
    dec_ = cx_.get('decisoes') or {}; exig_ = {'D%d' % i_ for i_ in range(34, 41)}
    decisoes_ok_ = bool(set(dec_) == exig_ and all(dec_.get(d_) == DL_.DECISOES.get(d_) and str(dec_.get(d_) or '').strip() for d_ in exig_))
    leitura_ok_ = bool(cx_.get('leituras') == DL_.LEITURA_V406 and 'ONTO' in str(DL_.LEITURA_V406.get('estatuto')) and len(cu.get('leituras_do_operador') or []) == len(DL_.FRASES_V406))
    ressalvas_ok_ = bool(cx_.get('ressalvas') == list(DL_.RESSALVAS_V406) and len(DL_.RESSALVAS_V406) == 8)
    contagens_ok_ = bool(cx_.get('n_falas') == len(ec_) and cx_.get('n_bandeiras') == FJ_['n_flags'] and cx_.get('n_modulos') == DL_.N_BUNDLE)
    checks_cu_ok_ = bool(cu.get('checks')) and all(c_.get('ok') is True for c_ in cu.get('checks'))
    import guarda_frases_v406 as GF_
    moldura_ok_ = bool(all(not GF_.violacoes(json.dumps({k_: (core.get(n_) or {}).get(k_) for k_ in ('verdict', 'estatuto', 'scope', 'limites', 'diz', 'nao_diz')}, ensure_ascii=False)) for n_ in REG_FIXOS) and (GF_.controle_negativo() or {}).get('ok') is True)
    kh_ok_ = bool(kh.get('all_verified') is True and kh.get('does_not_gate_core') is True and bool(_ev(ESP, 'kh_n1_cobertura_v406')) and kh.get('verdict') == _ev(ESP, 'kh_n1_cobertura_v406') and bool(kh.get('checks')) and all(c_.get('ok') is True for c_ in kh.get('checks')) and not GUARDA.search(str(kh.get('verdict') or '')))
    cu_ok_ = bool(verb_ok_ and checks_cu_ok_ and pares_ok_ and cu.get('all_verified') is True and cu.get('does_not_gate_core') is True and erratas_ok_ and decisoes_ok_ and leitura_ok_ and ressalvas_ok_ and contagens_ok_ and todas_op_ and moldura_ok_
                  and bool(_ev(ESP, 'cunhagens_v406')) and cu.get('verdict') == _ev(ESP, 'cunhagens_v406') and not GUARDA.search(str(cu.get('verdict') or '')))
    V['cunhagens'] = {'n': len(vb_), 'ok': cu_ok_, 'verbatim_ok': verb_ok_, 'todas_do_operador': todas_op_, 'checks_ok': checks_cu_ok_, 'n_checks': len(cu.get('checks') or []), 'verdict': cu.get('verdict'), 'kernel_ok': pares_ok_, 'erratas_ok': erratas_ok_, 'n_erratas': len(err_),
                      'decisoes_ok': decisoes_ok_, 'n_decisoes': len(dec_), 'leitura_ok': leitura_ok_, 'ressalvas_ok': ressalvas_ok_, 'contagens_ok': contagens_ok_, 'moldura_ok': moldura_ok_, 'kh_ok': kh_ok_}
    if not (verb_ok_ and checks_cu_ok_ and pares_ok_ and cu.get('all_verified') is True and cu.get('does_not_gate_core') is True and contagens_ok_ and cu.get('verdict') == _ev(ESP, 'cunhagens_v406')):
        P.append('cunhagens_v406: as inscricoes embutidas nao sao as de CANDIDATO_v406.json (sha256, embedded_ok, 23 falas), ou as checagens do registro, ou as contagens, ou o veredito diferem do ensaio a seco')
    if not todas_op_:
        P.append('cunhagens_v406: as inscricoes de 02/11 tem de ser TODAS falas do operador (OPERADOR_02nov_*): nesta versao nao ha inscricao da gerencia')
    if not erratas_ok_:
        P.append('cunhagens_v406: as erratas E14 a E17 (assinadas pela gerencia c1, em nome proprio) ausentes ou diferentes de delta_v406.ERRATAS_V406')
    if not decisoes_ok_:
        P.append('cunhagens_v406: as decisoes D34 a D40 da gerencia ausentes ou diferentes de delta_v406.DECISOES')
    if not (leitura_ok_ and ressalvas_ok_):
        P.append('cunhagens_v406: a leitura [ONTO] de 02/11 (estatutos), as 31 frases do operador ou as 8 ressalvas ausentes ou diferentes de delta_v406 (LEITURA_V406, FRASES_V406, RESSALVAS_V406)')
    if not moldura_ok_:
        P.append('a MOLDURA falhou: alguma frase proibida num registro novo da v406 (guarda das frases) ou o controle negativo da guarda falhou')
    if not kh_ok_:
        P.append('kh_n1_cobertura_v406 nao selou como o ensaio a seco (selo, veredito, checagens, nao move o gate)')
    # os registros por spec da v405 (cunhagens_v404 e kh_n1_cobertura_v404, RECRIADOS): iguais aos selados'''

END_CUNH = '    # os registros por spec da v405 (cunhagens_v404 e kh_n1_cobertura_v404, RECRIADOS): iguais aos selados'


def rodar(A):
    nome = "leitura_v406.py"
    txt, crlf, raw = A.le(nome)
    if A.pula(nome, txt):
        return
    t = A.entre(txt, "# [PREPARACAO v406", "import glob, hashlib, json, os, re, sys, datetime", A.NOTA_ADAPT + "\n" + HEADER)
    t = A.entre(t, 'REG_FUNCAO = ("ponte_da_massa_v405"', "SIDECAR_RE = re.compile", CONST)
    t = A.sub(t, "def ler():\n    P = []", EV)
    t = A.sub(t, "REG_TODOS = tuple(dict.fromkeys(tuple(REG_FIXOS) + tuple(ESP.get('registros_v405') or ())))", "REG_TODOS = tuple(REG_FIXOS)")
    # as linhas [v406] do stdout
    t = A.sub(t, "    if len([l for l in out.splitlines() if '[v405]' in l]) < 1:\n        P.append('o stdout nao tem a linha [v405]')\n", "    if len([l for l in out.splitlines() if '[v405]' in l]) < 1:\n        P.append('o stdout nao tem a linha [v405]')\n" + STD6)
    t = A.sub(t, "if '[v405] AVISO' in l or '[v404] AVISO' in l", "if '[v406] AVISO' in l or '[v405] AVISO' in l or '[v404] AVISO' in l")
    t = A.sub(t, "(os oito registros com funcao, os registros por spec, os registros recriados da v405,", "(o registro com funcao do fechamento, os registros por spec, os registros recriados da v405,")
    t = A.entre(t, "    RF_ = ESP.get('registros_funcao_v406') or {}", "    for r_, e_ in (('selo_pela_propria_tecnologia_v399'", RF)
    t = A.sub(t, "+ tuple((n_, (RF_.get(k_) or {}).get('verdict')) for k_, n_ in PEDRA_DE.items()):", "+ tuple((n_, _ev(ESP, n_)) for n_ in REG_V405C[:8]) + (('fechamento_v406', _ev(ESP, 'fechamento_v406')),):")
    # m_s5 -> acrescenta m_s6
    ancora_s5 = "esta ausente ou difere do ensaio a seco (%s)' % repr(m_s5.groups()[1:] if m_s5 else 'ausente'))\n"
    t = A.sub(t, ancora_s5, ancora_s5 + M_S6)
    # os TREZE da v405 recriados
    t = A.sub(t, "    V['reg399'] = {}", V405C)
    # o bundle (no lugar dos modulos novos por pedra)
    t = A.entre(t, "    # v406: o modulo novo de kernel vem de ESPERADOS[bundle_sha256]", "    vs = core.get('varredura_e_sorry_v392') or {}", BUNDLE)
    t = A.sub(t, "for k, v in (ESP.get('cunhagens') or {}).items()}", "for k, v in (CM.get('cunhagens') or {}).items()}")
    t = A.sub(t, "os CINCO registros novos (tres com FUNCAO, dois por spec)", "os TRES registros novos (um com FUNCAO, dois por spec)")
    # as quatro chaves
    t = A.entre(t, "    kf_ = (core.get('kernel_formalization') or {})\n    rf_ = core.get('rede_fock_v394') or {}", "    # o registro teste_de_veracidade_fase9_v397 (o QUADRO do topo le os numeros dele)", CHAVES)
    # as ancoras (no lugar do laco das oito pedras)
    t = A.entre(t, "    V['pedras_kernel'] = {}; kernel_ok_ = {}", "    # o selo pela propria tecnologia (registro com FUNCAO): conferido por inteiro", ANCORAS)
    ls = t.split("\n"); idx = [i for i, l in enumerate(ls) if l.startswith("    # as OITO pedras no kernel do rito:")]
    assert len(idx) == 1
    ls[idx[0]] = "    # v406: o trio, o axiom_report e a proveniencia do kernel do rito (as OITO ANCORAS do fecho e as bandeiras do bundle, abaixo); nenhum numero e' digitado"
    t = "\n".join(ls)
    # o fechamento (no lugar dos registros com funcao das pedras)
    t = A.entre(t, "    # os DOIS registros com FUNCAO das pedras da v406 (projecao, jo8v32)", "    # a errata de F2b (registro com FUNCAO, SEM pedra)", FECHO)
    # os registros com funcao recriados (v402, v403, v404 e agora as oito da v405)
    t = A.sub(t, "for fkey_, FUN_ in (('fun402', FUN_V402), ('fun405', FUN_V405), ('fun405b', FUN_V405B)):", "for fkey_, FUN_ in (('fun402', FUN_V402), ('fun405', FUN_V405), ('fun405b', FUN_V405B), ('fun405c', FUN_V405C)):")
    t = A.sub(t, "bool(EV2_.get(nome_)) and R_.get('verdict') == EV2_.get(nome_)", "bool(_ev(ESP, nome_)) and R_.get('verdict') == _ev(ESP, nome_)")
    t = A.entre(t, "    # as CINCO pedras SELADAS da v403 e da v405 seguem no kernel do Nos com o sha256 selado", "    # a falsidade da inercia (v401, registro com FUNCAO) RECRIADA pelo rito", PEDRAS13)
    # cunhagens_v406 / kh (no lugar de cunhagens_v405, campos, ga e gap)
    t = A.entre(t, "    # cunhagens_v405: as falas do operador de 30/10 a 01/11 por sha256", END_CUNH, CUNH + "\n")
    # os resumos do selo primario
    t = A.sub(t, "sreg5_ = selo.get('registros_v405') or {}", "sreg5_ = selo.get('registros_v405') or {}; sreg6_ = selo.get('registros_v406') or {}")
    t = A.sub(t, "+ tuple(FUN_V405.values()) + tuple(FUN_V402.values()) + ('bandeiras_do_gate_v403',))", "+ tuple(FUN_V405.values()) + tuple(FUN_V402.values()) + ('bandeiras_do_gate_v403',) + tuple(FUN_V405C.values()))")
    velho5 = "and bool(ESP.get('registros_v405')) and all((sreg5_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg5_.get(k_) or {}).get('verdict')) and (sreg5_.get(k_) or {}).get('all_verified') is True for k_ in ESP['registros_v405']))"
    novo5 = ("and bool(R405SPEC_) and all((sreg5_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg5_.get(k_) or {}).get('verdict')) and (sreg5_.get(k_) or {}).get('all_verified') is True for k_ in R405SPEC_)\n"
             "                       and bool(R406SPEC_) and all((sreg6_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg6_.get(k_) or {}).get('verdict')) and (sreg6_.get(k_) or {}).get('all_verified') is True for k_ in R406SPEC_))")
    t = A.sub(t, velho5, novo5)
    # o fecho do final: V['cunh_verdict'] usa `cu` e V['kh'] usa `kh` (definidos acima)
    A.grava(nome, t, crlf, raw)
