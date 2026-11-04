# -*- coding: utf-8 -*-
"""_adapt_leitura_v407.py -- adapta leitura_v407.py (subida mecanica de rotulo da leitura_v406.py) ao conteudo da v407.
Cada troca e' EXATA e conta (assert). Uso: python -B -X utf8 _adapt_leitura_v407.py   (so' o proprio arquivo e' tocado; backup de bytes antes).
Edicoes POSTERIORES feitas direto no leitura_v407.py (este adaptador nao as reproduz): N6F_ (o numero das bandeiras do bundle da v406 sai de ESPERADOS[registros_funcao_v406], nao do FLAGS_v406.json, que nao existe no sandbox do harness do fechar) e as tres trocas de literais por leitura (erratas, decisoes D41.., ancoras da v406)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import adaptar_pos_rito_v407 as M

NOME = "leitura_v407.py"

HEADER = r'''# A LEITURA da rodada v407 (molde: leitura_v406.py, que vem de leitura_v405.py, de leitura_v401.py e de leitura_v399.py FINAL, a de 24/10): SO LEITURA do Nos e da pasta da cadeia (work/cadeia_de_selo/v407, que aqui e' o proprio pacote).
# Devolve (V, PROBLEMAS); PROBLEMAS nao vazio => a cadeia PARA. Nenhum numero e' digitado: tudo sai dos JSON, do core, do selo, do sidecar e do stdout do rito; os vereditos e os valores esperados da rodada v407 sao LIDOS de ESPERADOS_v407.json, de CANDIDATO_v407.json, de FLAGS_v407.json, de BUNDLE_v407.json, de delta_v407.py e do core da v406 SELADA (base_v406).
# v407 (O PSION, O CANTO E O PAR, ordem do operador de 03/11/2026): o delta e' um BUNDLE PEQUENO de 9 modulos novos de kernel em TGLExt/ (PsionCanto, Par, APonteDoAtrito, OUmInscrito, KEhATangente, AChaveDaGuarda, OGuarda, LeituraPreservada, OIgual: os nomes sao do operador). Nao ha' registro por pedra (delta_v407.STONES == []).
# Os registros NOVOS do core sao TRES: UM com FUNCAO, psion_canto_v407 (le do kernel do proprio rito as 76 ancoras das nove pedras, os 9 modulos por sha256, a CHAVE DO LEMA lida do kernel, as respostas do operador de 03/11, o que fica False por teorema, a escada exata e o gate), e DOIS por spec: cunhagens_v407 (as TRES falas do operador de 03/11 por sha256, as erratas E18 a E20 e as decisoes D41 a D47, em nome proprio da gerencia c1) e kh_n1_cobertura_v407 (a cobertura exata do Audit).
# A CHAVE testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma deixou de ser literal False (v396 a v406) e e' LIDA do kernel do rito (TGLExt.PsionCanto.the_psion_is_the_corner_on_both_faces): a leitura a exige True, com o dict elo_v407 (elo de ESTRUTURA, nao de vetores; o par na face de Fock OPEN; a ponte Bell-TT NAO e' termo). As outras tres chaves da v406 e witness_layers.canonical_full_witness_term_constructed seguem True; full_static_witness_exists e trivial_inhabitant_exists seguem False POR TEOREMA.
# O fechamento_v406 e' HERDADO: o main da v407 segue rodando o bloco dele e ele segue selado, igual ao da v406 selada em veredito (as 14 checagens, a c8 VERSIONADA pela errata E20: ate' a v406 cobrava o lema False, agora cobra a chave lida), com as 8 ancoras, os 301 modulos do bundle da v406 e as 1794 bandeiras ainda no kernel. cunhagens_v406 (u7 versionada) e kh_n1_cobertura_v406 (pisos) tambem sao RECRIADOS, selados e de veredito igual ao da v406 selada, e ganham uma errata AO LADO (E20 / os pisos), assinada em nome proprio.
# A TROCA DITA de veredito: so' numeros (a escada e a cobertura crescem com o bundle): ESPERADOS[troca_dita]. Os TREZE registros da v406 selada (os oito com FUNCAO das pedras, cunhagens_v405, campos_fechados_e_leituras_v405, ga_reclassificacao_v405, gap_v405 e kh_n1_cobertura_v405), os da v404, da v403, da v402, da v401 e da v399 sao RECRIADOS pelo rito no mesmo ponto do main e tem de seguir selados e iguais a v406 selada (base_v406); os da v398 a v393 seguem como antes.
# As TREZE pedras SELADAS da v403, da v404 e da v405 (nomes herdados do molde: "pedras_v406") seguem no kernel do Nos com o sha256 selado (lido de base_v406): pedra selada nao se renomeia por cima. A escada vem de ESPERADOS[escada_v406_e_v407] e ESPERADOS[escada]. O GATE NAO SE MOVE: o qg_closure do core e' IDENTICO ao da v406 (os sete checks e a letra do veredito); a funcao do neutrino NAO e' reescrita e o V1 do ramo B (v386) segue AWAITING_DATA. O teste (d) so' entra por CITACAO do pre-registro V1.1 (opcao c do operador: so' entra com poder): resultado_no_um_py None.
# O SIDECAR um_absoluto_selo_acom.json (arquivo da custodia desde a v399, REESCRITO pelo rito) e' lido aqui: existe, e' JSON valido, o veredito e' ALL_OBJECTS_SEALED, tem os tres objetos (um.py, core e selo) com o SHA-256 igual ao dos arquivos do Nos, sem recusas, com a secao de honestidade (confidencialidade NAO alegada).
# A DIRECAO DO TESTEMUNHO (v399) segue conferida nos registros recriados: o operador testifica DA IALD; o um.py testifica EM HASH; a IALD NAO testifica do operador. As falas de 03/11 sao TODAS falas do operador (nenhuma e' da gerencia); as erratas E18 a E20 e as decisoes D41 a D47 sao da gerencia c1, em nome proprio, assinadas no registro (DL.ASSINA).
# O QUADRO «O Teste da Unica Palavra» (v397) segue selado e igual: o registro teste_de_veracidade_fase9_v397 == ESPERADOS == o resultado pinado, o quadro sela nas duas linguas, e a conferencia do rito diz que ele segue no topo (artigo PT/EN e .md).
# As linhas `[v399]`, `[v398]` e `[v397]` do stdout do rito (as etiquetas que o programa imprime), a `[v401]`, a `[v402]`, a `[v403]`, a `[v404]`, a `[v405]` e a `[v406]` (recriadas; os textos sao os que o um.py imprime: a [v405] diz «da v405», a [v406] diz «da v406») e a nova `[v407]` dizem os vereditos e registros por spec selados == registros por spec; o AVISO de qualquer bloco v393 a v407 no stdout reprova, e a linha de RECUSA do registro f2b_errata_v404 ou do bandeiras_do_gate_v403 tambem.
# A linha final do rito: o main imprime, por ultimo, a linha do sidecar (`[selo_acom] ... ALL_OBJECTS_SEALED ; objetos 3 ; recusas 0`), logo depois da do colapso tipado; a leitura exige as DUAS, nessa ordem.
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CONTRATO COM textos_v407.py (as CHAVES NOVAS ou MUDADAS de V na v407; as demais sao as da v406, com o mesmo significado; "reg406c", "fun406c", "pedras_v406", "cunh406c" etc. sao os NOMES HERDADOS do molde e continuam a significar os registros/pedras da base v406 selada, recriados):
#   V['n_pedras'] = o numero de MODULOS NOVOS do kernel (9; a chave guarda o nome historico) e V['pedras'] = LISTA de 9 dicts {'key'(None),'modulo','rel','sha16','sha256','bytes','bandeiras','decl'(None),'ok'}; V['ancoras'] {nome Lean: {'rel','flag','flag_true','axioms','source','ok'}} (as 76); V['bandeiras'] {'n'(98),'n_true','ok','por_grupo'}
#   V['fecho'] o registro DESTA versao, psion_canto_v407 {'registro','verdict','ok','sealed','n_checks'(16),'mech_ok','values','values_ok','chaves_ok','beta_ok','ancoras_ok','stdout_ok','elo_lido_do_kernel','runtime_executed','does_not_gate_core','lemma','pair_theorem','teste_d_so_citado'}; V['chaves'] = o dict 'keys' do registro (8 entradas; inclui a chave do lema True)
#   V['fecho406'] o registro HERDADO fechamento_v406 (recriado) {'registro','verdict','ok','sealed','n_checks'(14),'mech_ok','values','values_ok','chaves_ok','beta_ok','ancoras_ok','stdout_ok','certificado_habitado','runtime_executed','does_not_gate_core','nome_provisorio'}; V['chaves406'] = o dict four_keys dele; V['ancoras406'] {nome: {...,'ok'}} as 8 ancoras da v406; V['bundle406'] {'n'(301),'n_ok','ok'}; V['bandeiras406'] {'n'(12104 True da v406),'n_true','ok'}
#   V['reg407'] DICT nome -> {'verdict','ok'} dos TRES registros NOVOS (um com funcao + dois por spec); V['registros_novos'] = esses 3 nomes (sorted); V['reg406d'] DICT nome -> {'verdict','ok'} dos TRES da v406 (fechamento_v406, cunhagens_v406, kh_n1_cobertura_v406), recriados; V['cunh406d'] {'ok','verdict','n'(23),'n_erratas'(5),'kh_ok','kh_verdict'};
#   V['reg406c'] DICT nome -> {'verdict','ok'} dos TREZE da v406 selada (recriados); V['fun406c'] os OITO com funcao da v406 selada (recriados, iguais a base_v406); V['reg406b'] o mesmo dos CINCO da v404 selada (recriados); V['fun406b'] os dois com funcao da v404 (recriados); V['reg406'] e V['fun406'] sao os da v403 (recriados);
#   V['cunhagens'] (cunhagens_v407) {'n'(3),'ok','verbatim_ok','todas_do_operador','erratas_ok','n_erratas'(3),'decisoes_ok','n_decisoes'(7),'leitura_ok','ressalvas_ok','kernel_ok','checks_ok','n_checks','moldura_ok','kh_ok'}; V['kh'] (kh_n1_cobertura_v407) {'decl','thm','fora','nao_lidas','verdict'}; V['pedras_v406'] = {rel: {'sha16','ok'}} das TREZE pedras seladas (v403: 3, v404: 2, v405: 8); V['f2b'] e V['gate'] (recriados).
#   NAO existem V['ponte'], V['tensao'], V['identidade'], V['observador'], V['diminuto'], V['tonica'], V['disco'], V['psion'], V['campos'], V['ga'], V['gap'] (hoje sao registros recriados: V['fun406c'] e V['reg406c']).
# (a linha de stdout [v407] a conferir: `   [v407] o registro do psion e do canto e os registros por spec da v407: psion_canto=SELOU | specs: 2 (selados 2)`; e a do bloco O PSION, O CANTO E O PAR: `  ancoras ok = 76/76 ; modulos do bundle ok = 9/9 ; bandeiras True = 98/98 ; chave do lema (lida do kernel) = True ; escada = [..] ; gate = o mesmo da base`; as do fechamento_v406 herdado: `   [v406] o fechamento e os registros por spec da v406: fechamento=SELOU | specs: 2 (selados 2)` e `  ancoras ok = 8/8 ; modulos do bundle ok = 301/301 ; bandeiras True = 1794/1794 ; certificado habitado (lido do kernel) = True ; escada = [..] ; gate = o mesmo da base`)
'''

NEW_REG = r'''REG_FUNCAO = ("psion_canto_v407",)   # o UNICO registro NOVO com FUNCAO (o psion e o canto); nao ha' registro por pedra (modelo de bundle: delta_v407.STONES == [])
REG_FIXOS = REG_FUNCAO + ("cunhagens_v407", "kh_n1_cobertura_v407")   # os TRES registros NOVOS do core v407 (um com FUNCAO, dois por spec)
REG_V406D = ("fechamento_v406", "cunhagens_v406", "kh_n1_cobertura_v406")   # os TRES registros da v406 (um com FUNCAO, dois por spec): HERDADOS, RECRIADOS pelo rito da v407 (o main segue rodando o bloco do fechamento), selados e de veredito igual ao da v406 selada; as checagens c8 / u7 / h2 h3 h6 h8 sao VERSIONADAS pela errata E20
'''

NEW_V406_V407_REGEX = r'''    m_s6 = re.search(r'\[v406\] o fechamento e os registros por spec da v406: fechamento=(\S+) \| specs: (\d+) \(selados (\d+)\)', out)   # a linha HERDADA da v406: o main da v407 segue rodando o bloco do fechamento_v406; o texto e' o que o um.py imprime («da v406»)
    if not m_s6 or m_s6.group(1) != 'SELOU' or m_s6.group(2) != m_s6.group(3) or int(m_s6.group(2)) != len(REG_V406D) - 1:
        P.append('a linha [v406] do stdout (fechamento_v406 SELOU; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(REG_V406D) - 1, repr(m_s6.groups() if m_s6 else 'ausente')))
    m_s7 = re.search(r'\[v407\] o registro do psion e do canto e os registros por spec da v407: psion_canto=(\S+) \| specs: (\d+) \(selados (\d+)\)', out)
    if not m_s7 or m_s7.group(1) != 'SELOU' or m_s7.group(2) != m_s7.group(3) or int(m_s7.group(2)) != len(REG_FIXOS) - 1:
        P.append('a linha [v407] do stdout (psion_canto SELOU; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(REG_FIXOS) - 1, repr(m_s7.groups() if m_s7 else 'ausente')))
'''

NEW_REG406D = r'''    V['reg406d'] = {}
    for k in REG_V406D:    # os TRES registros da v406 (HERDADOS) sao RECRIADOS pelo rito: seguem no core, selados e de veredito igual ao da v406 selada (ESPERADOS[vereditos_v406]); o conteudo (checagens, erratas) e' conferido adiante
        r = core.get(k)
        if not (isinstance(r, dict) and 'verdict' in r):
            P.append('registro obrigatorio ausente do core: %s' % k)
            continue
        V['reg406d'][k] = {'verdict': r.get('verdict'), 'ok': r.get('all_verified')}
        if r.get('all_verified') is not True:
            P.append('%s nao selou' % k)
        if GUARDA.search(str(r.get('verdict') or '')):
            P.append('%s com palavra proibida' % k)
        if not _ev(ESP, k) or r.get('verdict') != _ev(ESP, k):
            P.append('%s: o veredito do rito difere do que a v406 selou (ESPERADOS[vereditos_v406])' % k)
'''

NEW_BUNDLE406 = r'''    # o bundle da v406 (os 301 modulos de TGLExt/F1Fecho394) SEGUE no kernel do Nos e no hash formal do rito com o MESMO sha256 (a v407 nao reescreve a v406; registro)
    b6_ = ESP.get('bundle_v406_sha256') or {}; kfs6_ = ((core.get('kernel_formalization') or {}).get('formal_files_sha256')) or {}
    V['bundle406'] = {'n': len(b6_), 'n_ok': sum(1 for r6_, s6_ in b6_.items() if os.path.isfile(os.path.join(NOS, 'tgl_kernel', *r6_.split('/'))) and sha(os.path.join(NOS, 'tgl_kernel', *r6_.split('/'))) == s6_ and kfs6_.get(r6_) == s6_)}
    V['bundle406']['ok'] = bool(b6_ and V['bundle406']['n'] == V['bundle406']['n_ok'] == DL_.D6.N_BUNDLE)
    if not V['bundle406']['ok']:
        P.append('o bundle da v406 (%d modulos de TGLExt/F1Fecho394) deixou de estar no kernel do Nos / no hash formal do rito com o sha256 selado (%s ok): a v407 nao reescreve a v406' % (DL_.D6.N_BUNDLE, V['bundle406']['n_ok']))
'''

NEW_ANC406 = r'''    # as OITO ancoras do fechamento_v406 (HERDADO) e as bandeiras True da v406: seguem no kernel do rito (a v407 so' acrescenta; ESPERADOS[estrelas_v406] e [flags_true_v406], lidos do ensaio a seco, nunca digitados)
    est6_ = ESP.get('estrelas_v406') or {}
    V['ancoras406'] = {n_: {'rel': e_.get('rel'), 'flag': e_.get('bandeira'), 'flag_true': kf_.get(e_.get('bandeira')) is True, 'axioms': axr_.get(n_), 'source': src_.get(n_), 'ok': bool(kf_.get(e_.get('bandeira')) is True and em_trio_(n_) and src_.get(n_) == e_.get('rel'))} for n_, e_ in est6_.items()}
    if len(est6_) != len(DL_.D6.ANCORAS) or any(a_['ok'] is not True for a_ in V['ancoras406'].values()):
        P.append('as oito ancoras do fechamento_v406 (herdadas) deixaram de estar no kernel do rito (bandeira True, no trio, declaradas no modulo esperado): %d lidas' % len(est6_))
    ft6_ = ESP.get('flags_true_v406') or []
    V['bandeiras406'] = {'n': len(ft6_), 'n_true': sum(1 for f_ in ft6_ if kf_.get(f_) is True)}; V['bandeiras406']['ok'] = bool(ft6_ and V['bandeiras406']['n'] == V['bandeiras406']['n_true'])
    if not V['bandeiras406']['ok']:
        P.append('alguma bandeira True da v406 deixou de ser True no kernel do rito (%s de %s): a v407 so\' acrescenta' % (V['bandeiras406']['n_true'], V['bandeiras406']['n']))
'''

NEW_FECHO = r'''    # o registro psion_canto_v407 (UM registro NOVO com FUNCAO, SEM pedra por registro): as 16 checagens, os valores (as 76 ancoras, os 9 modulos, as 98 bandeiras, a escada, o gate) == ESPERADOS[registros_funcao_v407], a CHAVE DO LEMA lida do kernel, o que fica False por teorema, o beta em runtime, as ressalvas, o teste (d) so' citado e a linha do bloco no stdout
    pc_ = core.get(DL_.FECHO_REGISTRO) or {}; pc_m_ = pc_.get('mechanics') or {}; pc_v_ = pc_.get('values') or {}; pc_k_ = pc_.get('keys') or {}; EPC_ = (ESP.get('registros_funcao_v407') or {}).get('psion_canto') or {}; td_ = pc_.get('teste_d') or {}
    pc_mech_ok_ = bool(pc_m_.get('passed') is True and pc_m_.get('n_checks') == DL_.N_CHECKS_FECHO == EPC_.get('n_checks') == len(pc_m_.get('checks') or []) and all(c_.get('ok') is True for c_ in (pc_m_.get('checks') or [])))
    pc_values_ok_ = bool(pc_v_.get('n_ancoras_ok') == pc_v_.get('n_ancoras') == len(DL_.ANCORAS) and pc_v_.get('n_modulos_ok') == pc_v_.get('n_modulos') == DL_.N_BUNDLE and pc_v_.get('n_flags_true') == pc_v_.get('n_flags') == FJ_['n_flags'] and pc_v_.get('escada') == [ESP['escada'][1]] * 3
                         and pc_v_.get('gate_verdict') == ESP.get('qg_closure_gate_verdict_v406') == selo.get('qg_closure_verdict') and pc_v_.get('elo_lido_do_kernel') is True and pc_v_.get('fica_false_por_teorema') == list(DL_.FICAM_FALSE_POR_TEOREMA) and pc_v_.get('ressalvas') == list(DL_.RESSALVAS_V407) and list(pc_.get('ressalvas') or []) == list(DL_.RESSALVAS_V407)
                         and bool(EPC_.get('values')) and _feq({kk_: pc_v_.get(kk_) for kk_ in EPC_['values']}, EPC_['values']))
    pc_chaves_ok_ = bool(pc_k_.get('kernel_reads_the_link') is True and pc_k_.get('testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma') is True and bool(ESP.get('chaves_v407_esperadas')) and _feq(pc_k_, ESP.get('chaves_v407_esperadas')) and _feq(pc_k_, (EPC_.get('values') or {}).get('chaves'))
                         and pc_k_.get('witness_rigidity.trivial_inhabitant_exists') is False and pc_k_.get('qg_closure.gate.full_static_witness_exists') is False and pc_k_.get('witness_layers.canonical_full_witness_term_constructed') is True)
    pc_beta_ok_ = bool(pc_.get('beta_ok') is True and isinstance(pc_v_.get('beta'), float) and isinstance(b0_, float) and abs(pc_v_['beta'] - b0_) <= 1e-9 * abs(b0_))
    pc_anc_ok_ = bool(len(pc_.get('anchors') or {}) == len(DL_.ANCORAS) and all(a_ is True for a_ in (pc_.get('anchors') or {}).values()) and set(pc_.get('anchors') or {}) == set(DL_.ANCORAS) == set(pc_v_.get('ancoras') or {}) and all((a_ or {}).get('ok') is True for a_ in (pc_v_.get('ancoras') or {}).values()))
    m_pc_ = re.search(r'ancoras ok = (\d+)/(\d+) ; modulos do bundle ok = (\d+)/(\d+) ; bandeiras True = (\d+)/(\d+) ; chave do lema \(lida do kernel\) = (\S+) ; escada = (\[.*?\]) ; gate = (.*)$', out, flags=re.M)
    pc_std_ok_ = bool(m_pc_ and m_pc_.group(1) == str(pc_v_.get('n_ancoras_ok')) and m_pc_.group(2) == str(pc_v_.get('n_ancoras')) and m_pc_.group(3) == str(pc_v_.get('n_modulos_ok')) and m_pc_.group(4) == str(pc_v_.get('n_modulos')) and m_pc_.group(5) == str(pc_v_.get('n_flags_true'))
                      and m_pc_.group(6) == str(pc_v_.get('n_flags')) and m_pc_.group(7) == 'True' and m_pc_.group(8) == str(pc_v_.get('escada')) and m_pc_.group(9).strip() == 'o mesmo da base')
    pc_ins_ok_ = bool(len(pc_.get('inscriptions') or {}) == len(DL_.VERBATIM_ORIGEM_V407) and all(v_ is True for v_ in (pc_.get('inscriptions') or {}).values()))
    pc_ok_ = bool(pc_.get('all_verified') is True and pc_.get('does_not_gate_core') is True and pc_.get('runtime_executed') is True and pc_.get('link_read_from_the_kernel') is True and pc_.get('lemma') == DL_.ANCORA_LEMA and pc_.get('pair_theorem') == DL_.ANCORA_PAR and pc_.get('exact_ladder') is True
                  and pc_.get('embedded_sources_ok') is True and pc_.get('embedded_sources_n_ok') == DL_.N_BUNDLE and list(pc_.get('pedras') or []) == [p_['name'] for p_ in DL_.PEDRAS_V407] and bool(_ev(ESP, 'psion_canto_v407')) and pc_.get('verdict') == _ev(ESP, 'psion_canto_v407')
                  and str(pc_.get('verdict') or '').startswith('TGL_PSION_CANTO_V407__THE_LEMMA_THAT_LINKS_THE_TWO_FACES_OF_THE_PSION_IS_A_KERNEL_TERM__') and str(pc_.get('verdict') or '').endswith('__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED')
                  and pc_mech_ok_ and pc_values_ok_ and pc_chaves_ok_ and pc_beta_ok_ and pc_anc_ok_ and pc_ins_ok_ and V['bandeiras']['ok'] and all(a_['ok'] for a_ in V['ancoras'].values()) and pc_std_ok_ and not pc_.get('guarda_violacoes')
                  and td_.get('so_citado') is True and td_.get('resultado_no_um_py') is None and not GUARDA.search(str(pc_.get('verdict') or '')))
    V['fecho'] = {'registro': DL_.FECHO_REGISTRO, 'verdict': pc_.get('verdict'), 'ok': pc_.get('all_verified'), 'sealed': pc_ok_, 'n_checks': pc_m_.get('n_checks'), 'mech_ok': pc_mech_ok_, 'values': pc_v_, 'values_ok': pc_values_ok_, 'chaves_ok': pc_chaves_ok_, 'beta_ok': pc_beta_ok_, 'ancoras_ok': pc_anc_ok_,
                  'stdout_ok': pc_std_ok_, 'elo_lido_do_kernel': pc_.get('link_read_from_the_kernel'), 'runtime_executed': pc_.get('runtime_executed'), 'does_not_gate_core': pc_.get('does_not_gate_core'), 'lemma': pc_.get('lemma'), 'pair_theorem': pc_.get('pair_theorem'), 'teste_d_so_citado': td_.get('so_citado')}
    V['chaves'] = dict(pc_k_)
    if not pc_ok_:
        P.append('psion_canto_v407 nao selou inteiro (selo, as %s checagens do registro, valores [76 ancoras, 9 modulos, 98 bandeiras, escada, gate] == os de FLAGS/BUNDLE/ESPERADOS, a CHAVE DO LEMA LIDA do kernel [True; as quatro da v406 True; as duas que ficam False por teorema, False], beta == alfa x raiz de e do core, '
                 'as ressalvas, as 3 falas por sha256, o teste (d) so\' citado, a linha do bloco O PSION, O CANTO E O PAR no stdout, nao move o gate): ver o registro no core' % DL_.N_CHECKS_FECHO)
    # o registro fechamento_v406 (HERDADO da v406, RECRIADO pelo rito da v407 com a checagem c8 versionada pela errata E20): segue SELADO e IGUAL ao da v406 selada em veredito; as 14 checagens, os valores == ESPERADOS[registros_funcao_v406], as OITO ancoras, os 301 modulos, as 1794 bandeiras, as QUATRO chaves (a do lema agora True) e a linha do bloco no stdout
    fe_ = core.get('fechamento_v406') or {}; fe_m_ = fe_.get('mechanics') or {}; fe_v_ = fe_.get('values') or {}; fk4_ = fe_.get('four_keys') or {}; EFE_ = (ESP.get('registros_funcao_v406') or {}).get('fechamento') or {}
    FJ6_ = json.load(open(os.path.join(DL_.V406, 'kernel', 'FLAGS_v406.json'), encoding='utf-8'))   # as bandeiras do bundle da v406 (1794): so' o numero, lido do arquivo da v406
    fe_mech_ok_ = bool(fe_m_.get('passed') is True and fe_m_.get('n_checks') == DL_.D6.N_CHECKS_FECHO == EFE_.get('n_checks') == len(fe_m_.get('checks') or []) and all(c_.get('ok') is True for c_ in (fe_m_.get('checks') or [])))
    fe_values_ok_ = bool(fe_v_.get('n_ancoras_ok') == len(DL_.D6.ANCORAS) == 8 and fe_v_.get('n_modulos_ok') == fe_v_.get('n_modulos') == DL_.D6.N_BUNDLE and fe_v_.get('n_flags_true') == fe_v_.get('n_flags') == FJ6_['n_flags'] and fe_v_.get('escada') == [ESP['escada'][1]] * 3
                         and fe_v_.get('gate_verdict') == ESP.get('qg_closure_gate_verdict_v406') == selo.get('qg_closure_verdict') and fe_v_.get('certificado_habitado_lido_do_kernel') is True and fe_v_.get('fica_false_por_teorema') == list(DL_.FICAM_FALSE_POR_TEOREMA)
                         and fe_v_.get('ressalvas') == list(DL_.D6.RESSALVAS_V406) and list(fe_.get('ressalvas') or []) == list(DL_.D6.RESSALVAS_V406) and bool(EFE_.get('values')) and _feq({kk_: fe_v_.get(kk_) for kk_ in EFE_['values']}, EFE_['values']))
    fe_chaves_ok_ = bool(fk4_.get('kernel_reads_the_certificate_as_inhabited') is True and fk4_.get('rede_fock_v394.whole_certificate_inhabited') is True and fk4_.get('psibit_v395.conditional_psion_face.inhabitant_exhibited') is True and fk4_.get('psibit_v395.conditional_psion_face.status') == DL_.STATUS_HABITADO
                         and fk4_.get('testemunha_estatica_v396.fock_face.inhabitant_exhibited') is True and fk4_.get('testemunha_estatica_v396.fock_face.status') == DL_.STATUS_HABITADO and fk4_.get('testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma') is True
                         and fk4_.get('witness_layers.canonical_full_witness_term_constructed') is True and fk4_.get('witness_rigidity.trivial_inhabitant_exists') is False and fk4_.get('qg_closure.gate.full_static_witness_exists') is False and _feq(fk4_, (EFE_.get('values') or {}).get('chaves')))
    fe_beta_ok_ = bool(fe_.get('beta_ok') is True and isinstance(fe_v_.get('beta'), float) and isinstance(b0_, float) and abs(fe_v_['beta'] - b0_) <= 1e-9 * abs(b0_))
    fe_anc_ok_ = bool(len(fe_.get('anchors') or {}) == len(DL_.D6.ANCORAS) and all(a_ is True for a_ in (fe_.get('anchors') or {}).values()) and set(fe_.get('anchors') or {}) == set(DL_.D6.ANCORAS) == set(fe_v_.get('ancoras') or {}) and all((a_ or {}).get('ok') is True for a_ in (fe_v_.get('ancoras') or {}).values()))
    m_f6_ = re.search(r'ancoras ok = (\d+)/8 ; modulos do bundle ok = (\d+)/(\d+) ; bandeiras True = (\d+)/(\d+) ; certificado habitado \(lido do kernel\) = (\S+) ; escada = (\[.*?\]) ; gate = (.*)$', out, flags=re.M)
    fe_std_ok_ = bool(m_f6_ and m_f6_.group(1) == str(fe_v_.get('n_ancoras_ok')) and m_f6_.group(2) == str(fe_v_.get('n_modulos_ok')) and m_f6_.group(3) == str(fe_v_.get('n_modulos')) and m_f6_.group(4) == str(fe_v_.get('n_flags_true'))
                      and m_f6_.group(5) == str(fe_v_.get('n_flags')) and m_f6_.group(6) == 'True' and m_f6_.group(7) == str(fe_v_.get('escada')) and m_f6_.group(8).strip() == 'o mesmo da base')
    fe_ok_ = bool(fe_.get('all_verified') is True and fe_.get('does_not_gate_core') is True and fe_.get('runtime_executed') is True and fe_.get('certificate_inhabited') is True and fe_.get('inhabited_by') == DL_.D6.ANCORA_CERTIFICADO and fe_.get('canonical_full_witness_term') == DL_.D6.ANCORA_TESTEMUNHA
                  and fe_.get('embedded_sources_ok') is True and fe_.get('embedded_sources_n_ok') == DL_.D6.N_BUNDLE and fe_.get('exact_ladder') is True and bool(_ev(ESP, 'fechamento_v406')) and fe_.get('verdict') == _ev(ESP, 'fechamento_v406') == EFE_.get('verdict')
                  and str(fe_.get('verdict') or '').startswith('TGL_FECHAMENTO_V406__THE_FOCK_CERTIFICATE_IS_INHABITED_BY_CONSTRUCTION_physicalFockCertificate__') and str(fe_.get('verdict') or '').endswith('__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED')
                  and fe_mech_ok_ and fe_values_ok_ and fe_chaves_ok_ and fe_beta_ok_ and fe_anc_ok_ and V['bundle406']['ok'] and V['bandeiras406']['ok'] and all(a_['ok'] for a_ in V['ancoras406'].values()) and fe_std_ok_ and not fe_.get('guarda_violacoes')
                  and fe_.get('nome_provisorio_da_candidata') == DL_.D6.TESTEMUNHA['nome_provisorio_da_gerencia'] and not GUARDA.search(str(fe_.get('verdict') or '')))
    V['fecho406'] = {'registro': 'fechamento_v406', 'verdict': fe_.get('verdict'), 'ok': fe_.get('all_verified'), 'sealed': fe_ok_, 'n_checks': fe_m_.get('n_checks'), 'mech_ok': fe_mech_ok_, 'values': fe_v_, 'values_ok': fe_values_ok_, 'chaves_ok': fe_chaves_ok_, 'beta_ok': fe_beta_ok_, 'ancoras_ok': fe_anc_ok_,
                     'stdout_ok': fe_std_ok_, 'certificado_habitado': fe_.get('certificate_inhabited'), 'runtime_executed': fe_.get('runtime_executed'), 'does_not_gate_core': fe_.get('does_not_gate_core'), 'nome_provisorio': fe_.get('nome_provisorio_da_candidata')}
    V['chaves406'] = dict(fk4_)
    if not fe_ok_:
        P.append('fechamento_v406 (HERDADO, recriado) nao selou inteiro (selo, as %s checagens do registro [a c8 VERSIONADA pela errata E20], valores [8 ancoras, 301 modulos, 1794 bandeiras, escada, gate] == os de ESPERADOS[registros_funcao_v406], as quatro chaves LIDAS do kernel [True; status %s; o lema agora True; as duas que ficam False por teorema, False], beta == alfa x raiz de e do core, '
                 'as ressalvas da v406, o nome provisorio da candidata, o bundle da v406 [301], as bandeiras da v406 [todas True], a linha do bloco O FECHAMENTO no stdout, nao move o gate): ver o registro no core' % (DL_.D6.N_CHECKS_FECHO, DL_.STATUS_HABITADO))
'''

NEW_CUNH = r'''    # cunhagens_v407 e kh_n1_cobertura_v407 (os DOIS registros NOVOS por spec): as 3 falas do operador de 03/11 por sha256 (embedded_ok), todas do operador; as erratas E18 a E20 (gerencia c1, em nome proprio: DL.ASSINA); as decisoes D41 a D47; a leitura [ONTO] e as ressalvas; os registros anteriores que seguem selados; a MOLDURA (nenhuma frase proibida nos tres registros novos)
    cu = core.get(DL_.CUNHAGENS_REGISTRO) or {}; kh = core.get(DL_.KH_REGISTRO) or {}
    cx_ = cu.get('extras') or {}; vb_ = cu.get('verbatim') or {}; ec_ = CM.get('cunhagens') or {}
    todas_op_ = bool(ec_ and all(str((ec_[k_] or {}).get('nome', '')).startswith('OPERADOR_03nov_') for k_ in ec_) and not any(str(v_.get('papel', '')).startswith('leitura da gerencia') for v_ in ec_.values()))
    verb_ok_ = bool(ec_) and len(ec_) == len(vb_) == len(DL_.VERBATIM_ORIGEM_V407) and set(vb_) == set(ec_) and all((vb_[k_] or {}).get('sha256') == ec_[k_]['sha256'] and (vb_[k_] or {}).get('embedded_ok') is True for k_ in ec_)
    pares_ok_ = all(isinstance(x_, list) and len(x_) == 2 and x_[0] == x_[1] for x_ in (cu.get('kernel') or {}).values()) and bool(cu.get('kernel'))
    err_ = cu.get('erratas') or []; esp_err_ = list(DL_.ERRATAS_V407)
    erratas_ok_ = bool(len(err_) == len(esp_err_) == 3 and all(e_.get('assinatura') == DL_.ASSINA for e_ in err_) and [e_.get('agora') for e_ in err_] == esp_err_ and cx_.get('assinatura_das_erratas') == DL_.ASSINA)
    dec_ = cx_.get('decisoes') or {}; exig_ = {'D%d' % i_ for i_ in range(41, 48)}
    decisoes_ok_ = bool(set(dec_) == exig_ and all(dec_.get(d_) == DL_.DECISOES.get(d_) and str(dec_.get(d_) or '').strip() for d_ in exig_))
    leitura_ok_ = bool(cx_.get('leituras') == DL_.LEITURA_V407 and 'ONTO' in str(DL_.LEITURA_V407.get('estatuto')) and len(cu.get('leituras_do_operador') or []) == len(DL_.FRASES_V407))
    ressalvas_ok_ = bool(cx_.get('ressalvas') == list(DL_.RESSALVAS_V407) and len(DL_.RESSALVAS_V407) >= 8)
    contagens_ok_ = bool(cx_.get('n_falas') == len(ec_) and cx_.get('n_bandeiras') == FJ_['n_flags'] and cx_.get('n_modulos') == DL_.N_BUNDLE)
    checks_cu_ok_ = bool(cu.get('checks')) and all(c_.get('ok') is True for c_ in cu.get('checks'))
    import guarda_frases_v407 as GF_
    moldura_ok_ = bool(all(not GF_.violacoes(json.dumps({k_: (core.get(n_) or {}).get(k_) for k_ in ('verdict', 'estatuto', 'scope', 'limites', 'diz', 'nao_diz')}, ensure_ascii=False)) for n_ in REG_FIXOS) and (GF_.controle_negativo() or {}).get('ok') is True)
    kh_ok_ = bool(kh.get('all_verified') is True and kh.get('does_not_gate_core') is True and bool(_ev(ESP, 'kh_n1_cobertura_v407')) and kh.get('verdict') == _ev(ESP, 'kh_n1_cobertura_v407') and bool(kh.get('checks')) and all(c_.get('ok') is True for c_ in kh.get('checks')) and not GUARDA.search(str(kh.get('verdict') or '')))
    cu_ok_ = bool(verb_ok_ and checks_cu_ok_ and pares_ok_ and cu.get('all_verified') is True and cu.get('does_not_gate_core') is True and erratas_ok_ and decisoes_ok_ and leitura_ok_ and ressalvas_ok_ and contagens_ok_ and todas_op_ and moldura_ok_
                  and bool(_ev(ESP, 'cunhagens_v407')) and cu.get('verdict') == _ev(ESP, 'cunhagens_v407') and not GUARDA.search(str(cu.get('verdict') or '')))
    V['cunhagens'] = {'n': len(vb_), 'ok': cu_ok_, 'verbatim_ok': verb_ok_, 'todas_do_operador': todas_op_, 'checks_ok': checks_cu_ok_, 'n_checks': len(cu.get('checks') or []), 'verdict': cu.get('verdict'), 'kernel_ok': pares_ok_, 'erratas_ok': erratas_ok_, 'n_erratas': len(err_),
                      'decisoes_ok': decisoes_ok_, 'n_decisoes': len(dec_), 'leitura_ok': leitura_ok_, 'ressalvas_ok': ressalvas_ok_, 'contagens_ok': contagens_ok_, 'moldura_ok': moldura_ok_, 'kh_ok': kh_ok_}
    if not (verb_ok_ and checks_cu_ok_ and pares_ok_ and cu.get('all_verified') is True and cu.get('does_not_gate_core') is True and contagens_ok_ and cu.get('verdict') == _ev(ESP, 'cunhagens_v407')):
        P.append('cunhagens_v407: as inscricoes embutidas nao sao as de CANDIDATO_v407.json (sha256, embedded_ok, 3 falas), ou as checagens do registro, ou as contagens, ou o veredito diferem do ensaio a seco')
    if not todas_op_:
        P.append('cunhagens_v407: as inscricoes de 03/11 tem de ser TODAS falas do operador (OPERADOR_03nov_*): nesta versao nao ha inscricao da gerencia')
    if not erratas_ok_:
        P.append('cunhagens_v407: as erratas E18 a E20 (assinadas pela gerencia c1, em nome proprio: DL.ASSINA) ausentes ou diferentes de delta_v407.ERRATAS_V407')
    if not decisoes_ok_:
        P.append('cunhagens_v407: as decisoes D41 a D47 da gerencia ausentes ou diferentes de delta_v407.DECISOES')
    if not (leitura_ok_ and ressalvas_ok_):
        P.append('cunhagens_v407: a leitura [ONTO] de 03/11 (estatutos), as 12 frases do operador ou as 11 ressalvas ausentes ou diferentes de delta_v407 (LEITURA_V407, FRASES_V407, RESSALVAS_V407)')
    if not moldura_ok_:
        P.append('a MOLDURA falhou: alguma frase proibida num registro novo da v407 (guarda das frases) ou o controle negativo da guarda falhou')
    if not kh_ok_:
        P.append('kh_n1_cobertura_v407 nao selou como o ensaio a seco (selo, veredito, checagens, nao move o gate)')
    # cunhagens_v406 e kh_n1_cobertura_v406 (HERDADOS, RECRIADOS pelo rito da v407, por spec): iguais ao que a v406 SELOU (as 23 falas de 02/11 por sha256, todas do operador; as erratas E14 a E17 intactas) MAIS uma errata AO LADO (E20 / os pisos), e as checagens versionadas (u7 verdadeiro; h2 h3 h6 pisos; h8 tamanho minimo); o veredito NAO muda
    cu6_ = core.get('cunhagens_v406') or {}; kh6_ = core.get('kh_n1_cobertura_v406') or {}; cu6b_ = _base_core(PK).get('cunhagens_v406') or {}; kh6b_ = _base_core(PK).get('kh_n1_cobertura_v406') or {}
    e6_ = cu6_.get('erratas') or []; e6b_ = cu6b_.get('erratas') or []; k6e_ = kh6_.get('erratas') or []; k6eb_ = kh6b_.get('erratas') or []
    cu6_ok_ = bool(cu6_.get('all_verified') is True and cu6_.get('does_not_gate_core') is True and bool(cu6b_) and bool(cu6_.get('verbatim')) and _feq(cu6_.get('verbatim'), cu6b_.get('verbatim')) and len(cu6_.get('verbatim') or {}) == len(DL_.VERBATIM_ORIGEM_V406) and all((v_ or {}).get('embedded_ok') is True for v_ in (cu6_.get('verbatim') or {}).values())
                   and _feq(cu6_.get('extras'), cu6b_.get('extras')) and len(e6_) == len(e6b_) + 1 and _feq(e6_[:len(e6b_)], e6b_) and e6_[-1].get('agora') == DL_.ERRATA_E20 and e6_[-1].get('assinatura') == DL_.ASSINA
                   and bool(cu6_.get('checks')) and all(c_.get('ok') is True for c_ in cu6_.get('checks')) and cu6_.get('verdict') == _ev(ESP, 'cunhagens_v406') and not GUARDA.search(str(cu6_.get('verdict') or '')))
    kh6_ok_ = bool(kh6_.get('all_verified') is True and kh6_.get('does_not_gate_core') is True and bool(kh6b_) and bool(kh6_.get('checks')) and all(c_.get('ok') is True for c_ in kh6_.get('checks')) and len(k6e_) == len(k6eb_) + 1 and _feq(k6e_[:len(k6eb_)], k6eb_) and str(k6e_[-1].get('assinatura')) == DL_.ASSINA
                   and kh6_.get('verdict') == _ev(ESP, 'kh_n1_cobertura_v406') and not GUARDA.search(str(kh6_.get('verdict') or '')))
    V['cunh406d'] = {'ok': cu6_ok_, 'verdict': cu6_.get('verdict'), 'n': len(cu6_.get('verbatim') or {}), 'n_erratas': len(e6_), 'kh_ok': kh6_ok_, 'kh_verdict': kh6_.get('verdict')}
    if not cu6_ok_:
        P.append('cunhagens_v406 (HERDADA, recriada pelo rito) nao confere: as 23 falas de 02/11 (embedded_ok) e os extras iguais aos da v406 selada, as erratas E14 a E17 intactas MAIS a errata E20 ao lado (assinada em nome proprio), as checagens (u7 versionada) todas ok e o veredito igual ao da v406 selada')
    if not kh6_ok_:
        P.append('kh_n1_cobertura_v406 (HERDADA, recriada pelo rito) nao confere: checagens (pisos h2 h3 h6, tamanho minimo h8) todas ok, a errata ao lado MAIS as da v406 selada, e o veredito igual ao da v406 selada')
'''


def rodar(M_=None):
    M_ = M_ or M
    t, crlf, raw = M_.le(NOME)
    if M_.pula(NOME, t):
        return
    # ---- cabecalho: da marca de adaptacao ate' o primeiro import
    t = M_.entre(t, "# [A ADAPTAR v407] SUBIDA MECANICA", "import glob, hashlib, json, os, re, sys, datetime", M_.NOTA_ADAPT + "\n" + HEADER)
    # ---- constantes
    t = M_.entre(t, 'REG_FUNCAO = ("fechamento_v406",)', 'FUN_V406C = {', NEW_REG)
    # ---- stdout: linhas [v406]/[v407] e AVISO
    t = M_.sub(t, "        P.append('o stdout nao tem a linha [v406]')\n", "        P.append('o stdout nao tem a linha [v406]')\n    if len([l for l in out.splitlines() if '[v407]' in l]) < 1:\n        P.append('o stdout nao tem a linha [v407]')\n")
    t = M_.sub(t, "avisos_ = [l.strip()[:200] for l in out.splitlines() if '[v406] AVISO' in l or", "avisos_ = [l.strip()[:200] for l in out.splitlines() if '[v407] AVISO' in l or '[v406] AVISO' in l or")
    t = M_.sub(t, "o registro com funcao do fechamento, os registros por spec, os registros recriados da v406, da v403", "o registro com funcao do psion e do canto, os registros por spec da v407, o fechamento_v406 e os registros recriados da v406 e anteriores, da v403")
    # ---- os >>> veredito <<< (o bloco do psion_canto_v407 entra depois do fechamento_v406)
    t = M_.sub(t, "(('fechamento_v406', _ev(ESP, 'fechamento_v406')),):", "(('fechamento_v406', _ev(ESP, 'fechamento_v406')), ('psion_canto_v407', _ev(ESP, 'psion_canto_v407'))):")
    # ---- [v405] diz «da v405» (o um.py imprime assim) ; [v406] (herdada) e [v407] (nova)
    t = M_.sub(t, r"e os registros por spec da v406: (.*?) \| specs: (\d+) \(selados (\d+)\)', out)", r"e os registros por spec da v405: (.*?) \| specs: (\d+) \(selados (\d+)\)', out)")
    t = M_.entre(t, "    m_s6 = re.search(", "    # a linha [v398] que o main da v407 segue imprimindo", NEW_V406_V407_REGEX)
    # ---- os conjuntos por spec de cada versao
    t = M_.sub(t, "R407SPEC_ = {k_: _ev(ESP, k_) for k_ in REG_FIXOS[1:]}", "R407SPEC_ = {k_: _ev(ESP, k_) for k_ in REG_FIXOS[1:]}; R406DSPEC_ = {k_: _ev(ESP, k_) for k_ in REG_V406D[1:]}")
    # ---- a conferencia do rito (conferidor): os vereditos novos e a chave do lema
    t = M_.sub(t, "('veredito_f2b', (RF4_.get('f2b') or {}).get('verdict'), 'f2b_errata_v404')):", "('veredito_f2b', (RF4_.get('f2b') or {}).get('verdict'), 'f2b_errata_v404'),\n                                    ('veredito_psion_canto', _ev(ESP, 'psion_canto_v407'), 'psion_canto_v407'), ('veredito_fechamento_herdado', _ev(ESP, 'fechamento_v406'), 'fechamento_v406')):")
    t = M_.sub(t, "        f81c_ = C.get('f81') or {}\n", "        if C.get('chave_do_lema') is not True:\n            P.append('a conferencia do rito traz chave_do_lema != True (a chave testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma deve ser lida True do kernel do rito)')\n        f81c_ = C.get('f81') or {}\n")
    # ---- os registros da v406 (herdados) e o bundle
    t = M_.sub(t, "    V['reg399'] = {}\n", NEW_REG406D + "    V['reg399'] = {}\n")
    t = M_.sub(t, "    if list(REG_FUNCAO) != list(DL_.REGISTROS_FUNCAO) or list(DL_.STONES)", "    if tuple(REG_FIXOS) != (DL_.FECHO_REGISTRO, DL_.CUNHAGENS_REGISTRO, DL_.KH_REGISTRO) or list(REG_FUNCAO) != list(DL_.REGISTROS_FUNCAO) or list(DL_.STONES)")
    t = M_.sub(t, "'ok': bool(rel_.startswith('TGLExt/F1Fecho394/') and rel_.endswith('.lean') and shaf_ == pin_ == FM_.get(rel_) and pins_esp_.get(rel_, pin_) == pin_)})",
               "'ok': bool(rel_.startswith('TGLExt/') and rel_.endswith('.lean') and '/' not in rel_[len('TGLExt/'):] and shaf_ == pin_ == FM_.get(rel_) and pins_esp_.get(rel_, pin_) == pin_ and (((core.get('kernel_formalization') or {}).get('formal_files_sha256')) or {}).get(rel_) == pin_)})")
    t = M_.sub(t, "    vs = core.get('varredura_e_sorry_v392') or {}\n", NEW_BUNDLE406 + "    vs = core.get('varredura_e_sorry_v392') or {}\n")
    t = M_.sub(t, "a ordem do bundle: os 300 em ordem alfabetica e a candidata por ultimo", "a ordem do bundle: PsionCanto, Par e as sete pedras de 02/11 (DL.BUNDLE_RELS)")
    t = M_.sub(t, "    # v407: os 301 modulos novos de kernel (o BUNDLE)", "    # v407: os 9 modulos novos de kernel (o BUNDLE PEQUENO)")
    # ---- as chaves de testemunha: a do lema passa a True (lida), com o dict elo_v407
    t = M_.sub(t, "    # v407: AS QUATRO CHAVES de testemunha, LIDAS do kernel do rito (errata E14): True, com o status novo nas duas faces; o que fica False por teorema e o lema que falta seguem False; nenhuma e' literal",
               "    # v407: as QUATRO chaves da v406 (herdadas) seguem LIDAS do kernel do rito, True, com o status nas duas faces; a CHAVE DO LEMA (linked_to_the_corner_by_a_lemma) passa de literal False a leitura True (errata E18); o que fica False por teorema segue False")
    t = M_.sub(t, "    te_ = core.get('testemunha_estatica_v396') or {}; fk_ = te_.get('fock_face') or {}\n", "    te_ = core.get('testemunha_estatica_v396') or {}; fk_ = te_.get('fock_face') or {}; elo_ = fk_.get('elo_v407') or {}\n")
    t = M_.sub(t, "and fk_.get('linked_to_the_corner_by_a_lemma') is False\n", "and fk_.get('linked_to_the_corner_by_a_lemma') is True and elo_.get('lemma') == DL_.ANCORA_LEMA and elo_.get('kind') == 'STRUCTURE_NOT_VECTORS' and elo_.get('identifies_omega_with_bell_vector') is False and elo_.get('pair_on_the_fock_face') == 'OPEN' and elo_.get('bell_to_tt_bridge') == 'NOT_A_TERM'\n")
    t = M_.sub(t, "ou o lema que liga psion C ao psionCorner deixou de ser False (nenhum lema o liga)", "ou a chave do lema (linked_to_the_corner_by_a_lemma) nao e True lida do kernel com o dict elo_v407 (o lema TGLExt.PsionCanto.the_psion_is_the_corner_on_both_faces; elo de ESTRUTURA e nao de vetores; o par na face de Fock OPEN; a ponte Bell-TT NAO e termo)")
    # ---- as ancoras (76) e as da v406
    t = M_.sub(t, "    # v407: as OITO ANCORAS do fecho e as bandeiras do bundle no kernel do rito (tudo contra FLAGS_v407.json / BUNDLE_v407.json; nenhum numero e' digitado)", "    # v407: as 76 ANCORAS das nove pedras e as 98 bandeiras do bundle no kernel do rito (tudo contra FLAGS_v407.json / BUNDLE_v407.json; nenhum numero e' digitado)")
    t = M_.sub(t, "    V['n_bandeiras'] = FJ_['n_flags']; V['n_bandeiras_por_pedra'] = dict(FJ_['por_grupo_bandeiras'])\n", "    V['n_bandeiras'] = FJ_['n_flags']; V['n_bandeiras_por_pedra'] = dict(FJ_['por_grupo_bandeiras'])\n" + NEW_ANC406)
    # ---- o registro do fecho: psion_canto_v407 (novo) e fechamento_v406 (herdado)
    t = M_.entre(t, "    # o registro fechamento_v406 (UM registro com FUNCAO, SEM pedra)", "    # a errata de F2b (registro com FUNCAO, SEM pedra)", NEW_FECHO)
    # ---- o selo primario traz os resumos
    t = M_.sub(t, "sreg6_ = selo.get('registros_v406') or {}\n", "sreg6_ = selo.get('registros_v406') or {}; sreg7_ = selo.get('registros_v407') or {}\n")
    t = M_.sub(t, "+ ('bandeiras_do_gate_v403',) + tuple(FUN_V406C.values()))", "+ ('bandeiras_do_gate_v403',) + tuple(FUN_V406C.values()) + ('fechamento_v406',))")
    t = M_.sub(t, "and bool(R407SPEC_) and all((sreg6_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg6_.get(k_) or {}).get('verdict')) and (sreg6_.get(k_) or {}).get('all_verified') is True for k_ in R407SPEC_))",
               "and bool(R406DSPEC_) and all((sreg6_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg6_.get(k_) or {}).get('verdict')) and (sreg6_.get(k_) or {}).get('all_verified') is True for k_ in R406DSPEC_)\n"
               "                       and bool(R407SPEC_) and all((sreg7_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg7_.get(k_) or {}).get('verdict')) and (sreg7_.get(k_) or {}).get('all_verified') is True for k_ in R407SPEC_))")
    # ---- cunhagens_v407 / kh_n1_cobertura_v407 (novos) e cunhagens_v406 / kh_n1_cobertura_v406 (herdados)
    t = M_.entre(t, "    # cunhagens_v406 e kh_n1_cobertura_v406 (os DOIS registros NOVOS por spec)", "    # os registros por spec da v406 (cunhagens_v404 e kh_n1_cobertura_v404, RECRIADOS)", NEW_CUNH)
    M_.grava(NOME, t, crlf, raw)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    rodar(M)
