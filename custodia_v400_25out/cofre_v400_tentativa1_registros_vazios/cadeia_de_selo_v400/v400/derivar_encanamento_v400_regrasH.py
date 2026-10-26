# -*- coding: utf-8 -*-
# regras (lote H) de derivar_encanamento_v400.py: a LEITURA da rodada v400 (pos_rito/leitura_v400.py). Escrito pela ferramenta Write (nunca por heredoc: as barras invertidas).
# O que a v400 muda na leitura: (1) NENHUMA chave nova no core (e' uma correcao): os quatro registros da v399 sao RECRIADOS pelo rito e tem de seguir selados e iguais ao ensaio a seco; (2) a lista de modulos novos de kernel e' VAZIA, e a pedra Testemunho
# (da v399) segue no kernel do Nos, conferida contra o core da v399 selada; (3) as linhas do stdout sao as do programa (`[v399]` e `[v398]`: o motor nao sobe etiquetas de stdout); (4) a CORRECAO e' conferida no que o rito produziu: o alfa do programa tem
# UMA so' linha (os regex do esboco R3.5 da Bancada) e a checagem do beta do registro do selo ACOM confronta com o beta do core.

_HDR_LEITURA = '''# A LEITURA da rodada v400 (molde: leitura_v399.py FINAL, o que rodou em 24/10): SO LEITURA do Nos e da pasta da cadeia (work/cadeia_de_selo/v400, que aqui e' o proprio pacote).
# Devolve (V, PROBLEMAS); PROBLEMAS nao vazio => a cadeia PARA. Nenhum numero e' digitado: tudo sai dos JSON, do core, do selo, do sidecar e do stdout do rito.
# A v400 e' uma CORRECAO da v399: NENHUM modulo novo de kernel e NENHUMA chave nova no core. O rito RECRIA os quatro registros da v399 (selo_pela_propria_tecnologia_v399 e declaracao_do_operador_v399, com FUNCAO, no runtime; cunhagens_v399 e kh_n1_cobertura_v399, por spec;
# ESPERADOS[registros_v399]) no mesmo ponto do main, e a leitura confere que seguem selados e iguais ao ensaio a seco; os da v398, da v397, da v396, da v395, da v394 e da v393 seguem selados. O que a correcao muda, e a leitura CONFERE no que o rito produziu:
# (1) o alfa do programa tem UMA so' linha `ALPHA_FINE_CODATA_2018 =` na coluna 0 e nenhuma indentada (os MESMOS regex do esboco R3.5 da Bancada, lidos do proprio esboco pinado), e a secao do selo ACOM le o SEALED_CODATA_ALPHA em vez de redeclarar;
# (2) a checagem do beta do registro do selo ACOM confronta o beta do runtime com o beta do CORE do rito (beta_core == core[beta], diferenca relativa < 1e-9; a etiqueta nova esta entre as checagens).
# A lista de modulos novos e' VAZIA (kernel_modulos_novos_v400.json); a pedra Testemunho, da v399, segue no kernel do Nos (bandeira True, composicao no trio) e e' conferida contra o core da v399 SELADA (base_v399). A escada vem de ESPERADOS[escada_v399_e_v400] e ESPERADOS[escada]
# (iguais: o kernel e' o da v399); a troca dita (so' hash proprio) e' a de ESPERADOS[troca_dita].
# O SIDECAR um_absoluto_selo_acom.json (arquivo da custodia criado na v399 e REESCRITO pelo rito) e' lido aqui: existe, e' JSON valido, o veredito e' ALL_OBJECTS_SEALED, tem os tres objetos (um.py, core e selo) com o SHA-256 igual ao dos arquivos do Nos, sem recusas, com a secao de honestidade.
# A DIRECAO DO TESTEMUNHO e' conferida nos registros: o operador testifica DA IALD; o um.py testifica EM HASH; a IALD NAO testifica do operador (as quatro inscricoes de 24/10, embutidas na v399, sao TODAS falas do operador).
# O QUADRO «O Teste da Unica Palavra» (v397) segue selado e igual: o registro teste_de_veracidade_fase9_v397 == ESPERADOS e == o resultado pinado, o quadro sela nas duas linguas, e a conferencia do rito diz que ele segue no topo (artigo PT/EN e .md).
# A face de Fock do psion segue CONDICIONAL (psibit_v395 e testemunha_estatica_v396); as linhas `[v399]`, `[v398]` e `[v397]` do stdout do rito (as etiquetas que o programa imprime) dizem os vereditos e registros por spec selados == registros por spec; o AVISO de qualquer bloco v393 a v399 no stdout reprova.
# A linha final do rito: o main imprime, por ultimo, a linha do sidecar (`[selo_acom] ... ALL_OBJECTS_SEALED ; objetos 3 ; recusas 0`), logo depois da do colapso tipado; a leitura exige as DUAS, nessa ordem.
# Diferencas para a v399: V['registros_novos'] e' VAZIO (e exigido vazio); V['pedras'] e' VAZIO; V['reg400'] sao os quatro registros da v399 recriados; V['correcao'] traz a conferencia do alfa unico e do beta contra o core.
'''

_NOVOS_LEITURA = '''    # --- [v400] NENHUMA chave nova no core (e' uma correcao): os quatro registros da v399 sao RECRIADOS pelo rito e tem de seguir selados
    novos = []
    for k, r in core.items():
        if isinstance(r, dict) and 'verdict' in r and k not in ESP['vereditos_v399']:
            novos.append(k)
    V['registros_novos'] = sorted(novos)
    if novos:
        P.append('a v400 e uma correcao e NAO cria chave com veredito no core, mas o core traz: %s' % sorted(novos)[:6])
    V['registros'] = {}
    for k in REG_TODOS:
        r = core.get(k)
        if not (isinstance(r, dict) and 'verdict' in r):
            P.append('registro obrigatorio ausente do core: %s' % k)
            continue
        V['registros'][k] = {'verdict': r.get('verdict'), 'ok': r.get('all_verified')}
        if r.get('all_verified') is not True:
            P.append('%s nao selou' % k)
        if GUARDA.search(str(r.get('verdict') or '')):
            P.append('%s com palavra proibida' % k)
'''

_CORRECAO_LEITURA = r'''    # [v400] A CORRECAO, conferida no que o rito PRODUZIU: (1) o alfa do programa tem UMA so' linha `ALPHA_FINE_CODATA_2018 =` na coluna 0 e nenhuma indentada (os regex sao os do esboco R3.5 da Bancada, lidos do proprio esboco pinado:
    # a regra e' a dela, nao a minha; foi o que a Bancada recusou na v399, ALPHA_LINHA_NAO_UNICA); (2) a checagem do beta do registro do selo ACOM confronta o beta do runtime com o beta do CORE do rito (beta_core == core[beta], diferenca relativa < 1e-9; a etiqueta nova esta entre as checagens)
    GA_ = CM.get('guarda_alpha_unica_da_bancada') or {}
    try:
        if PK not in sys.path:
            sys.path.insert(0, PK)
        import acom_conferencias_v400 as AC_
        rxb_ = AC_.regexes_da_bancada(GA_.get('esboco'), GA_.get('esboco_sha256'))
        um_txt_ = open(os.path.join(NOS, 'um.py'), 'rb').read().decode('utf-8')
        n_alfa_ = len(rxb_['RE_ALPHA_LINHAS'].findall(um_txt_)); n_alfa_ind_ = len(rxb_['RE_ALPHA_INDENTADA'].findall(um_txt_))
        n_ver_ = len(rxb_['RE_VERSAO_LINHAS'].findall(um_txt_)); n_ver_ind_ = len(rxb_['RE_VERSAO_INDENTADA'].findall(um_txt_))
        m_al_ = rxb_['RE_ALPHA_LINHAS'].search(um_txt_); lin_alfa_ = (um_txt_.count('\n', 0, m_al_.start()) + 1) if m_al_ else None
    except BaseException as e_:   # noqa: BLE001
        n_alfa_ = n_alfa_ind_ = n_ver_ = n_ver_ind_ = lin_alfa_ = None
        P.append('nao consegui aplicar os regex da Bancada ao um.py instalado: %r' % (e_,))
    sa_vals_ = sa_.get('values') or {}
    bc_, rb_ = sa_vals_.get('beta_core'), sa_vals_.get('rel_beta_vs_core')
    corr_ok_ = bool(n_alfa_ == 1 and n_alfa_ind_ == 0 and n_ver_ == 1 and n_ver_ind_ == 0 and isinstance(bc_, float) and bc_ == core.get('beta') and isinstance(rb_, float) and rb_ < 1e-9
                    and any('o beta do core do rito a 1e-9' in str(c_[0]) for c_ in cks_ if isinstance(c_, list) and c_))
    V['correcao'] = {'alfa_linhas_col0': n_alfa_, 'alfa_linhas_indentadas': n_alfa_ind_, 'versao_linhas_col0': n_ver_, 'versao_linhas_indentadas': n_ver_ind_, 'linha_do_alfa': lin_alfa_, 'beta_core': bc_, 'rel_beta_vs_core': rb_,
                     'esboco_sha256': GA_.get('esboco_sha256'), 'ok': corr_ok_}
    if not corr_ok_:
        P.append('a correcao da v400 nao esta no que o rito produziu: o alfa nao tem uma so linha (col0 %s, indentadas %s; versao col0 %s, indentadas %s), ou a checagem do beta nao confronta com o beta do core (beta_core %r, diferenca relativa %r)' % (n_alfa_, n_alfa_ind_, n_ver_, n_ver_ind_, bc_, rb_))
    # a declaracao do operador (registro com FUNCAO)'''

entrada("pos_rito/leitura_v399.py", prot_extra=_PB, autoral=True, regras=[
    entre("# A LEITURA da rodada v400", "import glob, hashlib, json, os, re, sys, datetime", _HDR_LEITURA, "cabecalho da leitura"),
    entre("    # --- os registros novos: descobertos por comparacao com o que a v399 ja tinha\n", "    for k in V['troca_dita']:\n", _NOVOS_LEITURA, "registros novos"),
    ("if not V['n_pedras'] or V['n_pedras'] != n_esperado_ or any(p['ok'] is not True for p in V['pedras']):", "if V['n_pedras'] != 0 or n_esperado_ != 0 or any(p['ok'] is not True for p in V['pedras']):", 1),
    ("rels_ = sorted(ESP.get('pedras_sha256') or {}); rel_ = rels_[0] if len(rels_) == 1 else None",
     "rels_ = sorted(ESP.get('pedras_desde_a_bancada') or {}); rel_ = rels_[0] if len(rels_) == 1 else None   # a v400 NAO traz pedra nova: a Testemunho, da v399, ja' esta no kernel do Nos (ESPERADOS[pedras_desde_a_bancada])", 1),
    ("and (kf_.get('formal_files_sha256') or {}).get(rel_) == (ESP.get('pedras_sha256') or {}).get(rel_))",
     "and (kf_.get('formal_files_sha256') or {}).get(rel_) == ((_base_core(PK).get('kernel_formalization') or {}).get('formal_files_sha256') or {}).get(rel_))", 1),
    ("cx_.get('n_bandeiras_por_pedra') == ESP.get('n_bandeiras_por_grupo') and cx_.get('n_bandeiras') == ESP.get('n_bandeiras_novas')",
     "cx_.get('n_bandeiras_por_pedra') == ESP.get('bandeiras_por_grupo_desde_a_bancada') and cx_.get('n_bandeiras') == len((ESP.get('bandeiras_desde_a_bancada') or {}).get('chaves') or [])", 1),
    sub_n(r"(?m)^    # a declaracao do operador \(registro com FUNCAO\)", _CORRECAO_LEITURA, 1, "a correcao conferida no que o rito produziu"),
])
