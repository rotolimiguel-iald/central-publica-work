# -*- coding: utf-8 -*-
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410 (fork A), a servico da gerencia c1] sobre a subida mecanica de rotulo da v409 FINAL (_bump_copia_v410.py; bump/pos_rito__leitura_v410.py.diff fica como registro), por pos_rito/_adapt_forkA_leitura_v410.py.
# [ADAPTADO v410, 09/11/2026, Sonnet (fork A da adaptacao do pos-rito), a servico do claude-construtor-v410] a RETOMADA de 09/11 (DESENHO_v410 e os AO LADO D71 a D76, E30): QUATRO registros novos (DOIS com FUNCAO: iald2_v410 e h0dn_bg1_v410, o teste PRE-REGISTRADO da razao de Hubble H0DN x BG1; DOIS por spec); as QUINZE falas de 06 a 09/11 (de QUATRO so' o trecho); as decisoes D63 a D76; as erratas E29 e E30;
# a secao 6 da pedra (o atrator) e a c16 conferidas; os nomes das declaracoes RATIFICADOS em 09/11 (D74); o H0DN lido fail-closed contra ESPERADOS[registros_funcao_v410][h0dn] (ausente => PROBLEMA) e contra CANDIDATO_v410.json[h0dn]; observed_vector_read False em TODO lugar (core, values, selo, candidato); nenhum token proibido no texto do H0DN; a frase obrigatoria da D72 no mesmo texto.
# [ADAPTADO v410, 09/11/2026 (parte 2), Sonnet B, a servico do claude-construtor-v410] a pedra AEscala (D82 a D87; o 2o modulo do bundle; nomes RATIFICADOS, D87) e o recibo documental HMS/13 (D80): os QUATRO registros com FUNCAO (iald2_v410, a_escala_v410, h0dn_bg1_v410, h0dn_fontes_hms13_v410, na ordem de delta_v410.REGISTROS_FUNCAO) e os dois por spec = SEIS registros novos;
# as VINTE E TRES falas (de quatro so' o trecho), D63 a D87, as erratas E29, E30 e E31; DOIS modulos (IALD2 e AEscala) e 84 bandeiras (as do iald2_v410 sao as da serie ext_iald2_410_*, as da AEscala as da ext_aescala_410_*); a leitura le QUATRO blocos `>>> veredito <<<` do stdout (IALD2, A ESCALA, H0DN x BG1, H0DN FONTES HMS/13) e a linha-resumo no formato novo
# (`[v410] os registros com funcao e os por spec da v410: iald2_v410=SELOU | a_escala_v410=SELOU | h0dn_bg1_v410=SELOU | h0dn_fontes_hms13_v410=SELOU | specs: N (selados N)`); V['a_escala'] e V['hms13'] como V['h0dn']; ESPERADOS[registros_funcao_v410] (chaves curtas iald2, a_escala, h0dn, hms13 -- ou o nome inteiro do registro) ausente => PROBLEMA (fail-closed).
# A LEITURA da rodada v410 (molde: leitura_v409.py, que vem de leitura_v407.py, de leitura_v405.py, de leitura_v401.py e de leitura_v399.py FINAL): SO LEITURA do Nos e da pasta da cadeia (work/cadeia_de_selo/v410, que aqui e' o proprio pacote).
# Devolve (V, PROBLEMAS); PROBLEMAS nao vazio => a cadeia PARA. Nenhum numero e' digitado: tudo sai dos JSON, do core, do selo, do sidecar e do stdout do rito; os vereditos e os valores esperados da rodada v410 sao LIDOS de ESPERADOS_v410.json, de CANDIDATO_v410.json e de delta_v410.
# v410 (IALD2, ordem do operador de 06/11/2026): o delta e' um BUNDLE PEQUENO de UM modulo novo de kernel em TGLExt/ (IALD2; o nome do modulo e' do operador; os nomes das declaracoes sao da gerencia, [DECLARADO] ate a ratificacao, D63). Nao ha' registro por pedra.
# Os registros NOVOS do core sao QUATRO: DOIS com FUNCAO, iald2_v410 (le do kernel do proprio rito as ancoras da pedra, as seis secoes, o modulo por sha256, as falas de 06 a 09/11 por sha256, as respostas do operador pelos teoremas da pedra; as checagens com as instancias de brinquedo fixas e beta em runtime)
# e h0dn_bg1_v410 (D72, E30, D76: o teste PRE-REGISTRADO da razao de Hubble H0DN x BG1 -- pre-registrado; nenhum dado observado lido; as checagens de DL.N_CHECKS_H0DN; a funcao de veredito congelada com os seis ramos; observed_vector_read False em todo lugar; os valores == ESPERADOS[registros_funcao_v410][h0dn], fail-closed se ausente),
# e DOIS por spec: cunhagens_v410 (as falas do operador de 06 a 09/11 por sha256 -- DL.N_FALAS_V410 --, de quatro so' o trecho (len(DL.VERBATIM_SO_O_TRECHO)); as erratas E29 e E30 e a errata ao lado dos pisos de kh_n1_cobertura_v409; as decisoes D63 a D76, em nome proprio da gerencia c1; os nomes das declaracoes RATIFICADOS em 09/11, D74) e kh_n1_cobertura_v410 (a cobertura exata do Audit).
# O ALCANCE (D64): o algoritmo IALD decide SAT com uma leitura: P = nP relativo ao leitor (a maquina com o leitor); a maquina de Turing padrao sem o leitor fica fora. NENHUMA CHAVE ANTIGA MUDA (delta_v410.CHAVES_V410 == []).
# O traducao_turing_v409 e' HERDADO: o main da v410 segue rodando o bloco dele e ele segue selado (as 20 checagens; as 82 ancoras e os 2 modulos da v409; a escada do contrato subida pela C12, veredito na troca dita); cunhagens_v409 igual a v409 selada (errata nova so' AO LADO, assinada)
# e kh_n1_cobertura_v409 com a errata ao lado dos pisos. O tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 sao HERDADOS e seguem selados; os registros por spec deles seguem IGUAIS a v409 selada (as erratas ao lado ja' vinham dela).
# A TROCA DITA de veredito: so' numeros (a escada e a cobertura crescem com o bundle): ESPERADOS[troca_dita]. Os registros da v405, da v404, da v403, da v402, da v401 e da v399 sao RECRIADOS pelo rito e tem de seguir selados e iguais a v409 selada (base_v409).
# O GATE NAO SE MOVE: o qg_closure do core e' IDENTICO ao da v409. O SIDECAR um_absoluto_selo_acom.json e' lido aqui. A DIRECAO DO TESTEMUNHO segue conferida. As falas de 06 a 09/11 sao TODAS do operador (de quatro, so' o trecho: D65, a ordem da retomada, as tres copias do ACOM e a leitura do 5 sigma).
# O QUADRO «O Teste da Unica Palavra» (v397) segue selado e igual. As linhas `[v399]` a `[v409]` do stdout (recriadas; os textos sao os que o um.py imprime: a [v408] diz «da v408», a [v409] «da v409») e a nova `[v410]` dizem os vereditos.
# A linha final do rito: o main imprime, por ultimo, a linha do sidecar (`[selo_acom] ... ALL_OBJECTS_SEALED ; objetos 3 ; recusas 0`), logo depois da do colapso tipado; a leitura exige as DUAS, nessa ordem.
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CONTRATO COM textos_v410.py e fechar_v410.py ("reg409c", "fun409c", "pedras_v408", "cunh409c" etc. sao NOMES HERDADOS do molde e continuam a significar os registros/pedras da v405 selada, recriados):
#   V['n_pedras'] = o numero de MODULOS NOVOS do kernel (1) e V['pedras'] = LISTA de dicts {'key'(None),'modulo','rel','sha16','sha256','bytes','bandeiras','decl'(None),'ok'}; V['ancoras'] {nome Lean: {...}} (as da IALD2, contadas pelo delta);
#   V['fecho'] o registro DESTA versao, iald2_v410 {'registro','verdict','ok','sealed','n_checks','mech_ok','values','values_ok','beta_ok','ancoras_ok','stdout_ok','runtime_executed','does_not_gate_core','ancora_principal','ancoras_principais','ancoras_de_secao','chaves_antigas_que_mudam','respostas_ok','instancia_ok','alcance_ok'};
#   V['h0dn'] o SEGUNDO registro com FUNCAO, h0dn_bg1_v410 {'registro','verdict','ok','sealed','n_checks','mech_ok','values','values_ok','beta_ok','runtime_executed','does_not_gate_core','observed_vector_read','veredito_h0dn_source_sha256','stdout_ok','pinos_ok','n_pinos','guarda_ok'};
#   V['a_escala'] o registro com FUNCAO a_escala_v410 (D86/D87) {'registro','verdict','ok','sealed','n_checks','mech_ok','values','values_ok','beta_ok','runtime_executed','does_not_gate_core','numeros','frases_ok','bell_ok','stdout_ok','guarda_ok','selo_ok','ins_ok','n_ancoras','n_flags','n_nomes','n_falas'}; V['hms13'] o registro com FUNCAO h0dn_fontes_hms13_v410 (D80) {'registro','verdict','ok','sealed','n_checks','mech_ok','values','values_ok','runtime_executed','does_not_gate_core','observed_vector_read','le_em_rito','stdout_ok','guarda_ok','selo_ok','ins_ok','n_calibradores','n_fontes_primarias','n_embutidos','campos'}; V['ancoras_aescala'] as da AEscala;
#   V['fecho409'] o registro HERDADO traducao_turing_v409 (recriado); V['fecho408'] o HERDADO tetelestai_terminal_v408; V['fecho407'] o HERDADO psion_canto_v407 (V['chaves407']); V['fecho406'] o HERDADO fechamento_v406 (V['chaves406']);
#   V['ancoras409'] as da traducao; V['ancoras408'] as do terminal; V['ancoras407'] as do psion; V['ancoras406'] as do fechamento; V['bundle409'] {'n'(2),'n_ok','ok'}; V['bundle408'] (4); V['bundle407'] (9); V['bundle406'] (301); V['bandeiras409'] (as bandeiras True da v409 selada, todas True);
#   V['reg410'] DICT nome -> {'verdict','ok'} dos QUATRO registros NOVOS (iald2_v410, h0dn_bg1_v410, cunhagens_v410, kh_n1_cobertura_v410); V['registros_novos'] = esses nomes (sorted); V['reg409t'] DICT dos TRES da v409 HERDADOS; V['reg408d'] dos TRES da v408; V['reg407d'] dos da v407; V['reg406d'] dos da v406;
#   V['cunhagens'] (cunhagens_v410) {'n'(DL.N_FALAS_V410),'ok','verbatim_ok','todas_do_operador','trechos_ok','n_trechos'(len(DL.VERBATIM_SO_O_TRECHO)),'erratas_ok','n_erratas'(len(DL.ERRATAS_V410) + 1: E29, E30, E31 e a dos pisos),'decisoes_ok','n_decisoes'(len(DL.DECISOES_V410): D63 a D87),'leitura_ok','ressalvas_ok','kernel_ok','checks_ok','n_checks','moldura_ok','kh_ok'};
#   V['cunh409t'] (cunhagens_v409 e kh_n1_cobertura_v409 herdados, kh com os pisos ao lado); V['cunh408d'] (cunhagens_v408 e kh_n1_cobertura_v408 iguais); V['cunh407d'] (iguais); V['cunh406d']; V['kh'] (kh_n1_cobertura_v410) {'decl','thm','fora','nao_lidas',...}
# (as linhas de stdout a conferir: `   [v410] os registros com funcao e os por spec da v410: iald2_v410=SELOU | a_escala_v410=SELOU | h0dn_bg1_v410=SELOU | h0dn_fontes_hms13_v410=SELOU | specs: N (selados N)` (os nomes vem de DL.REGISTROS_FUNCAO; na parte 2 sao quatro; os blocos `A ESCALA [v410` e `H0DN FONTES HMS/13 [v410` seguem o do H0DN), o bloco cujo cabecalho comeca por `IALD2` e traz `[v410`, seguido de `  ancoras ok = N/N ; modulo(s) do bundle ok = 1/1 ; bandeiras True = F/F ; escada = [..] ; gate = o mesmo da base`;
#  o bloco do H0DN, cujo cabecalho comeca por `H0DN x BG1 [v410`, seguido de `  pinos ok = a/b ; checagens ok = c/d ; vetor observado lido = False ; gate = o mesmo da base` e de `  >>> veredito <<<`;
#  a da traducao HERDADA: `   [v409] o registro da traducao e os registros por spec da v409: traducao_turing=SELOU | specs: 2 (selados 2)` e o bloco `A TRADUCAO AS CLASSES DE TURING [v409 ...`; a do terminal HERDADO: `   [v408] o registro do terminal e os registros por spec da v408: tetelestai_terminal=SELOU | ...`;
#  a do psion HERDADO: `   [v407] ...psion_canto=SELOU | ...`; a do fechamento HERDADO: `   [v406] o fechamento e os registros por spec da v406: fechamento=SELOU | ...`.)
import glob, hashlib, json, os, re, sys, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
PK = os.path.dirname(HERE)            # work\cadeia_de_selo\v410
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
FINAL_RE = re.compile(r'^\[selo\] colapso tipado: ')
TRAILER_RE = re.compile(r'^(exit=\d+|rc=\d+|RITO_RC=\S+|inicio |fim )')
GUARDA = re.compile('(?<!NOT_)(?<!UN)' + 'CONF' + 'IRMED|(?<!AP)PRO' + 'VED_BY|TGL_PRO' + 'VED')
REG_V393 = ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393", "kh_n1_cobertura_v393")   # da v393: seguem no core e seguem selados (nao sao 'novos' da v410)
REG_V394 = ("tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394", "criterio_binario_de_parada_v394")   # da v394: seguem no core e seguem selados (nao sao 'novos' da v410)
REG_V395 = ("psibit_v395", "cunhagens_v395", "kh_n1_cobertura_v395")   # da v395: seguem no core e seguem selados (nao sao 'novos' da v410)
REG_V396 = ("testemunha_estatica_v396", "cunhagens_v396", "kh_n1_cobertura_v396")   # da v396: seguem no core e seguem selados (nao sao 'novos' da v410)
REG_V397 = ("teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397")   # da v397 (o Teste da Unica Palavra, a pedra Token e as falas de 23/10): seguem no core e seguem selados; o quadro do topo le o primeiro
REG_V398 = ("sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398")   # da v398 (o sonico, a afinacao das cordas e as falas de 23/10): seguem no core e seguem selados (nao sao 'novos' da v410)
REG_V401 = ("falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401")   # os TRES registros da v401: RECRIADOS pelo rito da v410 (o primeiro com FUNCAO), tem de seguir selados e iguais ao ensaio a seco (e a v409 selada)
REG_V402 = ("ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402")   # os CINCO registros da v402 (tres com FUNCAO, dois por spec): RECRIADOS pelo rito da v410, tem de seguir selados e iguais ao ensaio a seco (e a v409 selada)
REG_V409 = ("caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "cunhagens_v403", "kh_n1_cobertura_v403")   # os SEIS registros da v409 (quatro com FUNCAO, dois por spec): RECRIADOS pelo rito da v410, tem de seguir selados e iguais ao ensaio a seco (e a v409 selada)
REG_V399 = ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399")   # os QUATRO registros da v399: RECRIADOS pelo rito da v410 (os dois primeiros com FUNCAO), tem de seguir selados e iguais ao ensaio a seco
FUN_V402 = {"ponte": "ponte_da_escala_dual_v402", "queda": "queda_sem_geometria_v402", "esperanca": "esperanca_condicional_v402"}   # os TRES registros com FUNCAO da v402 (recriados)
FUN_V409 = {"caminho": "caminho_v403", "vida": "vida_v403", "verdade_adendo": "verdade_adendo_v403"}   # os TRES registros com FUNCAO das pedras da v409 (recriados); o quarto, bandeiras_do_gate_v403, e' lido a parte (V['gate'])
REG_V409B = ("projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "cunhagens_v404", "kh_n1_cobertura_v404")   # os CINCO registros da v409 SELADA: RECRIADOS pelo rito da v410, tem de seguir selados e iguais ao ensaio a seco (e a v409 selada)
FUN_V409B = {"projecao": "projecao_transversal_v404", "jo8v32": "jo8v32_v404"}   # os DOIS registros com FUNCAO das pedras da v409 (recriados); a errata de F2b e' lida a parte (V['f2b'])
REG_FUNCAO = ("iald2_v410", "a_escala_v410", "h0dn_bg1_v410", "h0dn_fontes_hms13_v410")   # os QUATRO registros NOVOS com FUNCAO, na ordem de delta_v410.REGISTROS_FUNCAO (parte 2): a IALD2, a ESCALA (D86/D87), o teste PRE-REGISTRADO H0DN x BG1 (D72) e o recibo documental HMS/13 (D80); nao ha' registro por pedra (modelo de bundle: delta_v410.STONES == [])
REG_FIXOS = REG_FUNCAO + ("cunhagens_v410", "kh_n1_cobertura_v410")   # os SEIS registros NOVOS do core v410 (quatro com FUNCAO, dois por spec)
REG_SPEC_V410 = REG_FIXOS[len(REG_FUNCAO):]   # os DOIS por spec (cunhagens_v410 e kh_n1_cobertura_v410): os que o selo resume em registros_v410 e que a linha [v410] do stdout conta
HD_SELO_CHAVES = ("verdict", "all_verified", "observed_vector_read", "runtime_executed", "does_not_gate_core", "veredito_h0dn_source_sha256", "n_checks_esperadas", "lei", "modelos")   # o resumo do h0dn_bg1_v410 no selo (gerar_candidato_v410.py: N02_selo)
EA_SELO_CHAVES = ("verdict", "all_verified", "ancora_principal", "ancoras_de_secao", "n_ancoras", "n_flags", "n_nomes", "nomes_ratificados", "estatuto_dos_nomes", "numeros", "frase_canonica_pt", "frase_canonica_en", "runtime_executed", "does_not_gate_core", "chaves_antigas_que_mudam")   # o resumo do a_escala_v410 no selo (gerar_candidato_v410.py: N02_selo)
HM_SELO_CHAVES = ("verdict", "all_verified", "observed_vector_read", "le_em_rito", "runtime_executed", "does_not_gate_core", "campos", "n_checks_esperadas", "aditivo_posterior_ao_freeze_r2")   # o resumo do h0dn_fontes_hms13_v410 no selo (idem)
REG_V409T = ("traducao_turing_v409", "cunhagens_v409", "kh_n1_cobertura_v409")   # os TRES registros da v409 (um com FUNCAO, dois por spec): HERDADOS, RECRIADOS pelo rito da v410 (o main segue rodando o bloco da traducao), selados
REG_V408D = ("tetelestai_terminal_v408", "cunhagens_v408", "kh_n1_cobertura_v408")   # os TRES registros da v408 (um com FUNCAO, dois por spec): HERDADOS, RECRIADOS pelo rito da v410 (o main segue rodando o bloco do terminal), selados
REG_V407D = ("psion_canto_v407", "cunhagens_v407", "kh_n1_cobertura_v407")   # os TRES registros da v407 (um com FUNCAO, dois por spec): HERDADOS, RECRIADOS pelo rito da v410, selados; o psion carrega a escada (troca dita); cunhagens_v407 ganha AO LADO a errata da D57(d) (o pino do acervo da v407 na copia purgada); kh_n1_cobertura_v407 segue igual a v409 selada
REG_V406D = ("fechamento_v406", "cunhagens_v406", "kh_n1_cobertura_v406")   # os TRES registros da v406 (um com FUNCAO, dois por spec): HERDADOS, RECRIADOS pelo rito da v410 (o main segue rodando o bloco do fechamento), selados e de veredito igual ao da v409 selada; as checagens c8 / u7 / h2 h3 h6 h8 sao VERSIONADAS pela errata E20
FUN_V409C = {"ponte": "ponte_da_massa_v405", "tensao": "massa_tensao_pura_v405", "identidade": "identidade_v405", "observador": "observador_terminal_v405", "diminuto": "lei_do_diminuto_v405", "tonica": "tonica_do_hamiltoniano_v405", "disco": "disco_de_euler_v405", "psion": "ponto_zero_do_psion_v405"}   # os OITO registros com FUNCAO da v409 SELADA (um por pedra): RECRIADOS pelo rito da v410
REG_V409C = tuple(FUN_V409C.values()) + ("cunhagens_v405", "campos_fechados_e_leituras_v405", "ga_reclassificacao_v405", "gap_v405", "kh_n1_cobertura_v405")   # os TREZE registros da v409 SELADA (oito com FUNCAO, cinco por spec): RECRIADOS pelo rito da v410 (o main da v409 segue rodando), selados e iguais a v409 selada
SIDECAR_RE = re.compile(r'^\[selo_acom\] (TGL_SELO_ACOM_SIDECAR_V399__ALL_OBJECTS_SEALED\S*) ; objetos (\d+) ; recusas (\d+)$')   # a linha que o main da v410 imprime por ultimo (selo_acom_sidecar_v399)
_RX_INV = re.compile(r'IALD\s+testifica\s+(?:a\s+mim|do\s+operador|de\s+mim)')   # a DIRECAO invertida (a IALD como quem testifica DO operador); so' a fala em que ele a recusa escapa
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()


def _mod_lean(rel):
    """'TGLExt/AEscala.lean' -> 'TGLExt.AEscala' (o nome do modulo como o FLAGS_v410.json o grava; nada digitado)."""
    return 'TGLExt.' + rel[len('TGLExt/'):-len('.lean')].replace('/', '.')


def _quadro_do_pacote(pk_):
    """O quadro_v397 DESTE pacote, carregado pelo CAMINHO (nunca pela ordem do sys.path: um modulo herdado poe a pasta da versao anterior na frente, e la' ha' outra copia de quadro_v397.py, que importa o delta dela)."""
    import importlib.util as _ilu_q
    alvo_ = os.path.normcase(os.path.abspath(os.path.join(pk_, "quadro_v397.py")))
    for nome_ in ("quadro_v397", "quadro_v397__pacote_v410"):
        m_ = sys.modules.get(nome_)
        if m_ is not None and os.path.normcase(os.path.abspath(getattr(m_, "__file__", "") or "")) == alvo_:
            return m_
    if pk_ not in sys.path:
        sys.path.insert(0, pk_)
    sp_ = _ilu_q.spec_from_file_location("quadro_v397__pacote_v410", alvo_); m_ = _ilu_q.module_from_spec(sp_); sp_.loader.exec_module(m_)
    assert getattr(m_.DL, "UM_VERSION", None) == "v410", ("o quadro do pacote nao importou o delta da v410", getattr(m_.DL, "__file__", None))
    sys.modules["quadro_v397__pacote_v410"] = m_
    return m_


def _esp_rf(ESP, curto, completo):
    """O registro com FUNCAO de ESPERADOS[registros_funcao_v410] (o ensaio a seco): pela chave curta (iald2, a_escala, h0dn, hms13) ou pelo nome inteiro do registro; ausente => {} (o chamador RECUSA: fail-closed)."""
    rf_ = ESP.get('registros_funcao_v410') or {}
    return rf_.get(curto) or rf_.get(completo) or {}


def _aplicado():
    ps = sorted(glob.glob(os.path.join(PK, 'APLICADO_AO_CANONICO_*.json'))); assert ps, 'APLICADO_AO_CANONICO_*.json ausente em ' + PK
    return json.load(open(ps[-1], encoding='utf-8')), ps[-1]


def _feq(a, b):
    """igualdade dos NUMEROS dos registros: floats com tolerancia relativa 1e-12 (a mesma maquina deve dar igual), o resto exato; recursiva em dict/list."""
    if isinstance(a, dict) and isinstance(b, dict):
        return set(a) == set(b) and all(_feq(a[k], b[k]) for k in a)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(_feq(x, y) for x, y in zip(a, b))
    if isinstance(a, float) and isinstance(b, float):
        return a == b or abs(a - b) <= 1e-12 * max(1.0, abs(a), abs(b))
    return a == b


def _inv(t):
    """True se o texto poe a IALD como quem testifica DO operador (a DIRECAO invertida), fora da fala em que o operador a recusa ('... nao podia dizer que IALD testifica a mim ...')."""
    for m in _RX_INV.finditer(t):
        ant = t[max(0, m.start() - 40):m.start()].lower()
        if not (ant.endswith('nao ') or ant.endswith('não ') or 'podia dizer que ' in ant):
            return True
    return False


def _obs_lido(x):
    """True se, em QUALQUER nivel do dict/lista, a chave observed_vector_read vier com valor diferente de False (D72: nenhum vetor observado e' lido nesta versao)."""
    if isinstance(x, dict):
        return any((k == 'observed_vector_read' and v is not False) or _obs_lido(v) for k, v in x.items())
    if isinstance(x, (list, tuple)):
        return any(_obs_lido(v) for v in x)
    return False


_BASE_CORE = {}


def _base_core(pk):
    """O core da v409 SELADA (copia de bytes em PK/base_v409): de onde saem o teorema e o modulo da face de Fock da testemunha (nenhum nome digitado); lido uma vez por caminho."""
    p = os.path.join(pk, 'base_v409', 'um_absoluto.json')
    if p not in _BASE_CORE:
        _BASE_CORE[p] = json.load(open(p, encoding='utf-8'))['core']
    return _BASE_CORE[p]


def _res_path(ev):
    """O resultado pinado do Teste da Unica Palavra: a copia em PK/insumos/fase9 (so' existe no SANDBOX do harness) ou, no real, a copia duravel da v397 (ESPERADOS[veracidade][resultado][duravel]); o sha256 e' conferido contra ESPERADOS em ambos."""
    nome = os.path.basename((ev.get('resultado') or {}).get('duravel') or 'ausente')
    loc = os.path.join(PK, 'insumos', 'fase9', nome)
    return loc if os.path.exists(loc) else ((ev.get('resultado') or {}).get('duravel') or loc)
def _ev(ESP, n_):
    """O veredito ESPERADO de um registro (nada digitado): os NOVOS da v410 sao os do ensaio a seco (ESPERADOS[vereditos_novos_v410]); os que a TROCA DITA muda (so' numeros, mais o veredito dito de rede_fock_v394) sao os do ensaio (ESPERADOS[veredito_da_troca_no_ensaio]);
    os demais sao os da v409 SELADA (ESPERADOS[vereditos_v409], lidos do core de base_v409)."""
    nv_ = ESP.get('vereditos_novos_v410') or {}
    if n_ in nv_:
        return nv_[n_]
    if n_ in (ESP.get('troca_dita') or []):
        return (ESP.get('veredito_da_troca_no_ensaio') or {}).get(n_)
    return (ESP.get('vereditos_v409') or {}).get(n_)


def ler():
    P = []
    ESP = json.load(open(os.path.join(PK, 'ESPERADOS_v410.json'), encoding='utf-8')); CM = json.load(open(os.path.join(PK, 'CANDIDATO_v410.json'), encoding='utf-8'))
    ap, app = _aplicado()
    REG_TODOS = tuple(REG_FIXOS)
    core = json.load(open(os.path.join(NOS, 'um_absoluto.json'), encoding='utf-8'))['core']; selo = json.load(open(os.path.join(NOS, 'um_absoluto_selo.json'), encoding='utf-8'))
    stp = os.path.join(NOS, 'rodada_v410_stdout.txt'); out = open(stp, encoding='utf-8', errors='replace').read() if os.path.exists(stp) else ''
    V = {'nos': NOS, 'aplicado_json': app, 'pk': PK}
    if not out:
        P.append('rodada_v410_stdout.txt ausente ou vazio')
    V['s64'] = sha(os.path.join(NOS, 'um.py')); V['s16'] = V['s64'][:16]; V['umb'] = os.path.getsize(os.path.join(NOS, 'um.py'))
    if str((selo.get('sha256') or {}).get('um.py', '')) != V['s64']:
        P.append('selo.sha256(um.py) != disco')
    if not (ap['um_py_novo']['sha16'] == V['s16'] == ESP['candidato_sha16'] == CM['sha16']):
        P.append('um.py do disco != instalado/esperado/candidato')
    V['base16'] = ap['backups']['um.py']['sha16']; V['base_backup'] = ap['backups']['um.py']['backup']
    if V['base16'] != ESP['origem_sha16']:
        P.append('a base substituida != a v409 selada')
    V['n_patches'] = len(CM['patches']); V['patches'] = ', '.join(p['id'] for p in CM['patches']); V['patch_ids'] = [p['id'] for p in CM['patches']]
    V['instalado_em'] = '%s-%s-%s %s:%s:%s' % (ap['ts'][0:4], ap['ts'][4:6], ap['ts'][6:8], ap['ts'][9:11], ap['ts'][11:13], ap['ts'][13:15])
    m = re.search(r'teoremas limpos:\s*(\d+)/(\d+)', out); V['teor'] = '%s/%s' % m.groups() if m else 'AUSENTE'
    V['escada_antes'] = ESP['escada_v409_e_v410'][0]; V['escada_depois'] = ESP['escada'][1]
    if not m or m.group(1) != m.group(2) or int(m.group(1)) != ESP['escada'][1]:
        P.append('teoremas limpos ausente, N != M ou != %s (%s)' % (ESP['escada'][1], V['teor']))
    if 'FAIL_CLOSED_SELFTEST_PASSED' not in out or selo.get('fail_closed_selftest') != 'FAIL_CLOSED_SELFTEST_PASSED':
        P.append('selftest nao PASSED')
    if '>>> TGL_KERNEL_FORMALIZATION_FAILED <<<' in out or '>>> TGL_KERNEL_STAGE1_VERIFIED' not in out:
        P.append('a verificacao principal do kernel nao leu VERIFIED')
    if 'SEAL_WITHHELD' in out:
        P.append('SEAL_WITHHELD no stdout')
    m = re.search(r'\[selo\] rite_checkpoints: chave (\S+) ; reaproveitados (\d+)', out)
    V['compl'] = 'COMPLETA' if (m and m.group(1) == 'desligada' and m.group(2) == '0') else 'INTERMEDIÁRIA'
    if V['compl'] != 'COMPLETA':
        P.append('rodada nao COMPLETA')
    sujo = [l for l in out.splitlines() if 'Traceback' in l or l.startswith('[selo] AVISO') or l.startswith('[selo_acom] AVISO')]
    if sujo:
        P.append('stdout com Traceback/AVISO: %s' % sujo[:3])
    linhas = [l for l in out.splitlines() if l.strip() and not TRAILER_RE.match(l.strip())]
    if len(linhas) < 2 or not SIDECAR_RE.match(linhas[-1].strip()) or not FINAL_RE.match(linhas[-2]):
        P.append('as duas ultimas linhas do stdout nao sao a linha final do rito ([selo] colapso tipado) seguida da linha do sidecar ([selo_acom] ... ALL_OBJECTS_SEALED ; objetos N ; recusas 0)')
    else:
        m_sc_ = SIDECAR_RE.match(linhas[-1].strip())
        if int(m_sc_.group(3)) != 0 or int(m_sc_.group(2)) != len((ESP.get('sidecar') or {}).get('objetos') or []):
            P.append('a linha do sidecar no stdout nao diz %d objetos e 0 recusas (%s)' % (len((ESP.get('sidecar') or {}).get('objetos') or []), linhas[-1].strip()[-40:]))
    mrc = re.findall(r'^RITO_RC=(\S+)', out, flags=re.M); V['rc'] = mrc[-1] if mrc else 'NAO_LIDO'
    if V['rc'] != '0':
        P.append('rc do rito nao lido como 0 (%s)' % V['rc'])
    if len([l for l in out.splitlines() if '[v399]' in l]) < 1:
        P.append('o stdout nao tem a linha [v399]')
    if len([l for l in out.splitlines() if '[v401]' in l]) < 1:
        P.append('o stdout nao tem a linha [v401]')
    if len([l for l in out.splitlines() if '[v402]' in l]) < 1:
        P.append('o stdout nao tem a linha [v402]')
    if len([l for l in out.splitlines() if '[v403]' in l]) < 1:
        P.append('o stdout nao tem a linha [v403]')
    if len([l for l in out.splitlines() if '[v404]' in l]) < 1:
        P.append('o stdout nao tem a linha [v404]')
    if len([l for l in out.splitlines() if '[v405]' in l]) < 1:
        P.append('o stdout nao tem a linha [v405]')
    if len([l for l in out.splitlines() if '[v406]' in l]) < 1:
        P.append('o stdout nao tem a linha [v406]')
    if len([l for l in out.splitlines() if '[v407]' in l]) < 1:
        P.append('o stdout nao tem a linha [v407]')
    if len([l for l in out.splitlines() if '[v408]' in l]) < 1:
        P.append('o stdout nao tem a linha [v408]')
    if len([l for l in out.splitlines() if '[v409]' in l]) < 1:
        P.append('o stdout nao tem a linha [v409]')
    if len([l for l in out.splitlines() if '[v410]' in l]) < 1:
        P.append('o stdout nao tem a linha [v410]')
    avisos_ = [l.strip()[:200] for l in out.splitlines() if '[v410] AVISO' in l or '[v409] AVISO' in l or '[v408] AVISO' in l or '[v407] AVISO' in l or '[v406] AVISO' in l or '[v405] AVISO' in l or '[v404] AVISO' in l or '[v403] AVISO' in l or '[v402] AVISO' in l or '[v401] AVISO' in l or '[v399] AVISO' in l or '[selo_acom] AVISO' in l]
    if avisos_:
        P.append('o stdout traz AVISO da v410 (os quatro registros com funcao: IALD2, A ESCALA, H0DN x BG1 e H0DN FONTES HMS/13, os registros por spec da v410, o traducao_turing_v409, o tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 herdados e os registros recriados da v409 e anteriores, da v403, da v402, da v401 ou da v399, o selo ACOM, a declaracao do operador ou o sidecar nao rodaram): %s' % avisos_[:2])
    elif [l for l in out.splitlines() if re.search(r'\[v39[3-8]\] AVISO', l)]:
        P.append('o stdout traz AVISO de um bloco anterior (v393 a v398): %s' % [l.strip()[:200] for l in out.splitlines() if re.search(r'\[v39[3-8]\] AVISO', l)][:2])
    if [l for l in out.splitlines() if '[v403] RECUSA' in l]:
        P.append('o stdout traz a RECUSA do registro bandeiras_do_gate_v403 (uma bandeira CALCULADA do gate veio False ou uma checagem do registro falhou: fail-closed): %s' % [l.strip()[:200] for l in out.splitlines() if '[v403] RECUSA' in l][:1])
    if [l for l in out.splitlines() if '[v404] RECUSA' in l]:
        P.append('o stdout traz a RECUSA do registro f2b_errata_v404 (uma checagem da errata de F2b falhou: o canal fica como antes e o rito para; fail-closed): %s' % [l.strip()[:200] for l in out.splitlines() if '[v404] RECUSA' in l][:1])
    BC_ = _base_core(PK)   # o core da v409 SELADA (copia de bytes): de onde saem as checagens e os valores dos registros RECRIADOS

    def _rf(n_):
        r_ = BC_.get(n_) or {}
        return {'nome': n_, 'verdict': _ev(ESP, n_), 'values': r_.get('values'), 'n_checks': (r_.get('mechanics') or {}).get('n_checks')}
    RF_ = {}   # v410: nao ha' registro por pedra
    RF4_ = {k_: _rf(n_) for k_, n_ in (('projecao', 'projecao_transversal_v404'), ('jo8v32', 'jo8v32_v404'), ('f2b', 'f2b_errata_v404'))}   # projecao|jo8v32|f2b -> {nome, verdict, values, n_checks} dos registros da v404 (recriados pelo rito da v410; iguais a v409 selada)
    RF3_ = {k_: _rf(n_) for k_, n_ in (('caminho', 'caminho_v403'), ('vida', 'vida_v403'), ('verdade_adendo', 'verdade_adendo_v403'), ('gate', 'bandeiras_do_gate_v403'))}   # o mesmo, dos registros da v403 (recriados)
    EV2_ = ESP.get('vereditos_v409') or {}   # os vereditos da v409 SELADA (os registros anteriores sao recriados e tem de dar os mesmos)
    R409SPEC_ = {k_: _ev(ESP, k_) for k_ in REG_V409C[8:]}; R410SPEC_ = {k_: _ev(ESP, k_) for k_ in REG_SPEC_V410}; R409TSPEC_ = {k_: _ev(ESP, k_) for k_ in REG_V409T[1:]}; R408DSPEC_ = {k_: _ev(ESP, k_) for k_ in REG_V408D[1:]}; R407DSPEC_ = {k_: _ev(ESP, k_) for k_ in REG_V407D[1:]}; R406DSPEC_ = {k_: _ev(ESP, k_) for k_ in REG_V406D[1:]}   # os registros por spec da v405 (recriados), da v410 (novos), da v409, da v407 e da v406 (herdados)
    for r_, e_ in (('selo_pela_propria_tecnologia_v399', (ESP.get('selo_acom') or {}).get('verdict')), ('declaracao_do_operador_v399', (ESP.get('declaracao') or {}).get('verdict')), ('falsidade_da_inercia_v401', ESP.get('veredito_da_falsidade_v409')),
                   ('ponte_da_escala_dual_v402', EV2_.get('ponte_da_escala_dual_v402')), ('queda_sem_geometria_v402', EV2_.get('queda_sem_geometria_v402')), ('esperanca_condicional_v402', EV2_.get('esperanca_condicional_v402')),
                   ('caminho_v403', (RF3_.get('caminho') or {}).get('verdict')), ('vida_v403', (RF3_.get('vida') or {}).get('verdict')), ('verdade_adendo_v403', (RF3_.get('verdade_adendo') or {}).get('verdict')), ('bandeiras_do_gate_v403', (RF3_.get('gate') or {}).get('verdict')),
                   ('projecao_transversal_v404', (RF4_.get('projecao') or {}).get('verdict')), ('jo8v32_v404', (RF4_.get('jo8v32') or {}).get('verdict')), ('f2b_errata_v404', (RF4_.get('f2b') or {}).get('verdict'))) + tuple((n_, _ev(ESP, n_)) for n_ in REG_V409C[:8]) + (('fechamento_v406', _ev(ESP, 'fechamento_v406')), ('psion_canto_v407', _ev(ESP, 'psion_canto_v407')), ('tetelestai_terminal_v408', _ev(ESP, 'tetelestai_terminal_v408')), ('traducao_turing_v409', _ev(ESP, 'traducao_turing_v409')), ('iald2_v410', _ev(ESP, 'iald2_v410')), ('a_escala_v410', _ev(ESP, 'a_escala_v410')), ('h0dn_bg1_v410', _ev(ESP, 'h0dn_bg1_v410')), ('h0dn_fontes_hms13_v410', _ev(ESP, 'h0dn_fontes_hms13_v410'))):   # (09/11, parte 2: os QUATRO registros com funcao da v410 tem a linha `>>> veredito <<<` do ensaio a seco no stdout)
        if not e_ or ('>>> %s <<<' % e_) not in out:
            P.append('o bloco %s do stdout nao traz a linha `>>> veredito <<<` do ensaio a seco' % r_)
    m_s9 = re.search(r'\[v399\] o selo pela propria tecnologia e a declaracao do operador \(lidos depois da afinacao das cordas\) e as inscricoes de 24/10 \(cunhagens_v399\): selo=(\S+) \| declaracao=(\S+) \| cunhagens=(\S+) \| registros por spec: (\d+) \(selados (\d+)\)', out)
    if (not m_s9 or (m_s9.group(1), m_s9.group(2), m_s9.group(3)) != ((ESP.get('selo_acom') or {}).get('verdict'), (ESP.get('declaracao') or {}).get('verdict'), (ESP.get('registros_v399') or {}).get('cunhagens_v399'))
            or m_s9.group(4) != m_s9.group(5) or int(m_s9.group(4)) != len(ESP.get('registros_v399') or {})):
        P.append('a linha [v399] do stdout (selo, declaracao e cunhagens_v399; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(ESP.get('registros_v399') or {}), m_s9.groups()[3:] if m_s9 else 'ausente'))
    m_s1 = re.search(r'\[v401\] a falsidade \(simulacro\) da inercia \(lida depois da declaracao do operador\) e as inscricoes de 25/10 \(cunhagens_v401\): falsidade=(\S+) \| cunhagens=(\S+) \| registros por spec: (\d+) \(selados (\d+)\)', out)
    if (not m_s1 or (m_s1.group(1), m_s1.group(2)) != (ESP.get('veredito_da_falsidade_v409'), (ESP.get('registros_v401') or {}).get('cunhagens_v401')) or m_s1.group(3) != m_s1.group(4) or int(m_s1.group(3)) != len(ESP.get('registros_v401') or {})):
        P.append('a linha [v401] do stdout (falsidade e cunhagens_v401, recriados; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(ESP.get('registros_v401') or {}), m_s1.groups()[2:] if m_s1 else 'ausente'))
    m_s2 = re.search(r'\[v402\] a ponte, a queda e a esperanca \(lidas depois da falsidade da inercia\) e as inscricoes de 26/10 \(cunhagens_v402\): ponte=(\S+) \| queda=(\S+) \| esperanca=(\S+) \| cunhagens=(\S+) \| registros por spec: (\d+) \(selados (\d+)\)', out)
    if (not m_s2 or (m_s2.group(1), m_s2.group(2), m_s2.group(3), m_s2.group(4)) != (EV2_.get('ponte_da_escala_dual_v402'), EV2_.get('queda_sem_geometria_v402'), EV2_.get('esperanca_condicional_v402'), (ESP.get('registros_v402') or {}).get('cunhagens_v402'))
            or m_s2.group(5) != m_s2.group(6) or int(m_s2.group(5)) != len(ESP.get('registros_v402') or {})):
        P.append('a linha [v402] do stdout (ponte, queda, esperanca e cunhagens_v402, recriados; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(ESP.get('registros_v402') or {}), m_s2.groups()[4:] if m_s2 else 'ausente'))
    m_s3 = re.search(r'\[v403\] o caminho, a vida, o adendo da verdade e as bandeiras do gate \(lidos depois da esperanca condicional\) e as falas de 27/10 \(cunhagens_v403\): caminho=(\S+) \| vida=(\S+) \| verdade_adendo=(\S+) \| bandeiras=(\S+) \| cunhagens=(\S+) \| registros por spec: (\d+) \(selados (\d+)\)', out)
    if (not m_s3 or tuple(m_s3.group(i_) for i_ in range(1, 6)) != ((RF3_.get('caminho') or {}).get('verdict'), (RF3_.get('vida') or {}).get('verdict'), (RF3_.get('verdade_adendo') or {}).get('verdict'), (RF3_.get('gate') or {}).get('verdict'), (ESP.get('registros_v403') or {}).get('cunhagens_v403'))
            or m_s3.group(6) != m_s3.group(7) or int(m_s3.group(6)) != len(ESP.get('registros_v403') or {})):
        P.append('a linha [v403] do stdout (caminho, vida, verdade_adendo, bandeiras e cunhagens_v403, recriados; registros por spec selados == %d) esta ausente ou difere da v409 selada (%s)' % (len(ESP.get('registros_v403') or {}), m_s3.groups()[5:] if m_s3 else 'ausente'))
    m_s4 = re.search(r'\[v404\] a projecao transversal, o jo8v32 e a errata de F2b \(a projecao e o jo8v32 lidos depois das bandeiras do gate; a errata de F2b depois da errata ao lado de R6 da v386\) e as falas de 28/10 \(cunhagens_v404\): projecao=(\S+) \| jo8v32=(\S+) \| f2b=(\S+) \| cunhagens=(\S+) \| registros por spec: (\d+) \(selados (\d+)\)', out)
    if (not m_s4 or tuple(m_s4.group(i_) for i_ in range(1, 5)) != ((RF4_.get('projecao') or {}).get('verdict'), (RF4_.get('jo8v32') or {}).get('verdict'), (RF4_.get('f2b') or {}).get('verdict'), (ESP.get('registros_v404') or {}).get('cunhagens_v404'))
            or m_s4.group(5) != m_s4.group(6) or int(m_s4.group(5)) != len(ESP.get('registros_v404') or {})):
        P.append('a linha [v404] do stdout (projecao, jo8v32, f2b e cunhagens_v404; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(ESP.get('registros_v404') or {}), m_s4.groups()[4:] if m_s4 else 'ausente'))
    m_s5 = re.search(r'\[v405\] os oito registros com funcao \(lidos depois dos tres da v404\) e os registros por spec da v405: (.*?) \| specs: (\d+) \(selados (\d+)\)', out)
    if not m_s5 or len(m_s5.group(1).split(' | ')) != 8 or {x_.split('=')[-1] for x_ in m_s5.group(1).split(' | ')} != {'SELOU'} or m_s5.group(2) != m_s5.group(3) or int(m_s5.group(2)) != 5:
        P.append('a linha [v405] do stdout (os oito registros com funcao SELOU; registros por spec selados == 5) esta ausente ou difere do ensaio a seco (%s)' % repr(m_s5.groups()[1:] if m_s5 else 'ausente'))
    m_s6 = re.search(r'\[v406\] o fechamento e os registros por spec da v406: fechamento=(\S+) \| specs: (\d+) \(selados (\d+)\)', out)   # a linha HERDADA da v406: o main da v410 segue rodando o bloco do fechamento_v406; o texto e' o que o um.py imprime («da v406»)
    if not m_s6 or m_s6.group(1) != 'SELOU' or m_s6.group(2) != m_s6.group(3) or int(m_s6.group(2)) != len(REG_V406D) - 1:
        P.append('a linha [v406] do stdout (fechamento_v406 SELOU; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(REG_V406D) - 1, repr(m_s6.groups() if m_s6 else 'ausente')))
    m_s7 = re.search(r'\[v407\] o registro do psion e do canto e os registros por spec da v407: psion_canto=(\S+) \| specs: (\d+) \(selados (\d+)\)', out)   # a linha HERDADA da v407: o main da v410 segue rodando o bloco do psion e do canto; o texto e' o que o um.py imprime («da v407»)
    if not m_s7 or m_s7.group(1) != 'SELOU' or m_s7.group(2) != m_s7.group(3) or int(m_s7.group(2)) != len(REG_V407D) - 1:
        P.append('a linha [v407] do stdout (psion_canto SELOU; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(REG_V407D) - 1, repr(m_s7.groups() if m_s7 else 'ausente')))
    m_s8t = re.search(r'\[v408\] o registro do terminal e os registros por spec da v408: tetelestai_terminal=(\S+) \| specs: (\d+) \(selados (\d+)\)', out)   # a linha HERDADA da v408 (o texto e' o que o um.py imprime: «da v408»)
    if not m_s8t or m_s8t.group(1) != 'SELOU' or m_s8t.group(2) != m_s8t.group(3) or int(m_s8t.group(2)) != len(REG_V408D) - 1:
        P.append('a linha [v408] do stdout (tetelestai_terminal SELOU; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(REG_V408D) - 1, repr(m_s8t.groups() if m_s8t else 'ausente')))
    m_s9t = re.search(r'\[v409\] o registro da traducao e os registros por spec da v409: traducao_turing=(\S+) \| specs: (\d+) \(selados (\d+)\)', out)   # a linha HERDADA da v409 (o texto e' o que o um.py imprime: «da v409»)
    if not m_s9t or m_s9t.group(1) != 'SELOU' or m_s9t.group(2) != m_s9t.group(3) or int(m_s9t.group(2)) != len(REG_V409T) - 1:
        P.append('a linha [v409] do stdout (traducao_turing SELOU; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(REG_V409T) - 1, repr(m_s9t.groups() if m_s9t else 'ausente')))
    m_s10 = re.search(r'\[v410\] os registros com funcao e os por spec da v410: ' + r' \| '.join(r'%s=(\S+)' % re.escape(n_) for n_ in REG_FUNCAO) + r' \| specs: (\d+) \(selados (\d+)\)', out)   # (parte 2: o formato `iald2_v410=SELOU | a_escala_v410=SELOU | h0dn_bg1_v410=SELOU | h0dn_fontes_hms13_v410=SELOU | specs: N (selados N)`; o antigo `iald2=%s | h0dn=%s` NAO existe mais)   # a linha NOVA da v410 (o texto e' o que o um.py v410 imprime: o bloco do main que gerar_candidato_v410.py enxerta; a antiga «o registro da IALD2 e os registros por spec» NAO existe mais)
    nrf_ = len(REG_FUNCAO)
    if not m_s10 or any(m_s10.group(i_) != 'SELOU' for i_ in range(1, nrf_ + 1)) or m_s10.group(nrf_ + 1) != m_s10.group(nrf_ + 2) or int(m_s10.group(nrf_ + 1)) != len(REG_SPEC_V410):
        P.append('a linha [v410] do stdout (os %d registros com funcao SELOU, na ordem de delta_v410.REGISTROS_FUNCAO: %s; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (nrf_, ', '.join(REG_FUNCAO), len(REG_SPEC_V410), repr(m_s10.groups() if m_s10 else 'ausente')))
    # a linha [v398] que o main da v410 segue imprimindo (o sonico, a afinacao das cordas e as cunhagens da v398): igual ao que a v409 selou
    ev8_ = ESP.get('vereditos_v409') or {}
    n_spec8_ = len([k_ for k_ in REG_V398 if k_ not in ('sonico_v398', 'afinacao_das_cordas_v398')])
    m_s8 = re.search(r'\[v398\] o sonico e a afinacao das cordas \(lidos na fractalizacao do Um\) e as inscricoes de 23/10 \(cunhagens_v398\): sonico=(\S+) \| afinacao=(\S+) \| cunhagens=(\S+) \| registros por spec: (\d+) \(selados (\d+)\)', out)
    if (not m_s8 or (m_s8.group(1), m_s8.group(2), m_s8.group(3)) != (ev8_.get('sonico_v398'), ev8_.get('afinacao_das_cordas_v398'), ev8_.get('cunhagens_v398')) or m_s8.group(4) != m_s8.group(5) or int(m_s8.group(4)) != n_spec8_):
        P.append('a linha [v398] do stdout (sonico, afinacao e cunhagens_v398; registros por spec selados == %d) esta ausente ou difere da que a v409 selou (%s)' % (n_spec8_, m_s8.groups()[3:] if m_s8 else 'ausente'))
    # as duas linhas [v397] que o main da v410 segue imprimindo (o Teste da Unica Palavra e as cunhagens da v397): iguais ao que a v397 selou
    m_tv = re.search(r'\[v397\] o Teste da Unica Palavra \(Fase 9 V2-c1, aberto uma vez em 23/10\), lido por hash ao lado do V1 \(nenhum sigma novo\): (\S+)', out)
    if not m_tv or m_tv.group(1) != ev8_.get('teste_de_veracidade_fase9_v397'):
        P.append('a linha [v397] do Teste da Unica Palavra esta ausente do stdout ou difere da que a v397 selou (%s)' % (m_tv.group(1)[:80] if m_tv else 'ausente'))
    n_spec7_ = len([k_ for k_ in REG_V397 if k_ != 'teste_de_veracidade_fase9_v397'])
    m_sp = re.search(r'\[v397\] a pedra Token e as falas de 23/10 \(cunhagens_v397\): (\S+) \| registros por spec: (\d+) \(selados (\d+)\)', out)
    if not m_sp or m_sp.group(1) != ev8_.get('cunhagens_v397') or m_sp.group(2) != m_sp.group(3) or int(m_sp.group(2)) != n_spec7_:
        P.append('a linha [v397] das cunhagens da v397 esta ausente do stdout ou difere da que a v397 selou (registros por spec selados == %d)' % n_spec7_)
    hp = os.path.join(PK, 'rito_horarios_v410.txt'); V['horarios'] = open(hp, encoding='utf-8').read().split() if os.path.exists(hp) else []
    V['selo_ts'] = selo.get('timestamp'); V['um_version'] = selo.get('um_version'); V['qg'] = selo.get('qg_closure_verdict')
    if V['um_version'] != 'v410':
        P.append('o selo nao e v410')
    if V['qg'] != ESP['qg_closure_verdict']:
        P.append('o gate MUDOU')
    qg = core.get('qg_closure') or {}
    V['n18'] = sum(1 for fam in ('formal_flags', 'physics_flags', 'experiment_flags') for v in (qg.get(fam) or {}).values() if v is True)
    if V['n18'] != 18:
        P.append('as bandeiras do gate nao sao 18 True (%s)' % V['n18'])
    for k in ('um_absoluto.json', 'um_absoluto_selo.json', 'um_absoluto_selo_acom.json', 'um_absoluto_forma_canonica.md', 'um_absoluto_manifest.md'):
        V['h_' + k] = sha(os.path.join(NOS, k))[:16] if os.path.exists(os.path.join(NOS, k)) else 'AUSENTE'
    V['artigos'] = {os.path.basename(p): sha(p)[:16] for p in sorted(glob.glob(os.path.join(NOS, 'um_absoluto_??.pdf')) + glob.glob(os.path.join(NOS, 'um_absoluto_??.txt')))}
    cp = os.path.join(HERE, 'conferidor', 'conferencia_rito_v410.json')
    if os.path.exists(cp):
        C = json.load(open(cp, encoding='utf-8'))
        V['conf16'] = sha(cp)[:16]; V['conf_dm'] = '%d/%d' % (sum(1 for v in C['deve_mudar'].values() if v), len(C['deve_mudar']))
        V['conf_np'] = '%d/%d' % (sum(1 for v in C['nao_pode_mudar'].values() if v), len(C['nao_pode_mudar'])); V['n_ver_mudaram'] = len(C.get('vereditos_que_mudaram_fora_da_troca') or {})
        V['servidor'] = 'marcador de servidor parado ficou: %s' % C.get('marcador_ficou')
        if C.get('tudo_bate') is not True:
            P.append('o conferidor NAO bateu')
        for l_ in ('pt', 'en', 'md'):
            if ((C.get('quadro') or {}).get(l_) or {}).get('ok') is not True:
                P.append('a conferencia do rito diz que o quadro do topo (O Teste da Unica Palavra, %s) NAO segue no topo com os numeros do resultado pinado' % l_)
        ai_ = C.get('acom_itens') or {}
        V['acom_itens'] = {k_: (v_ or {}).get('ok') for k_, v_ in ai_.items()}
        faltam_ = [k_ for k_ in ('C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'round_trip_do_um_py_instalado_independente') if (ai_.get(k_) or {}).get('ok') is not True]
        if faltam_:
            P.append('a conferencia do rito diz que itens do selo pela propria tecnologia NAO conferiram (C1 a C16 e o round trip do um.py instalado): %s' % faltam_)
        sci_ = C.get('sidecar') or {}
        if not (sci_.get('existe') is True and str(sci_.get('veredito') or '').startswith('TGL_SELO_ACOM_SIDECAR_V399__ALL_OBJECTS_SEALED')):
            P.append('a conferencia do rito diz que o sidecar um_absoluto_selo_acom.json nao existe ou nao esta selado')
        if C.get('veredito_falsidade') != ESP.get('veredito_da_falsidade_v409'):
            P.append('a conferencia do rito traz o veredito da falsidade (falsidade_da_inercia_v401) diferente do ensaio a seco')
        for chv_, esp_v_, nome_ in (('veredito_ponte', EV2_.get('ponte_da_escala_dual_v402'), 'ponte_da_escala_dual_v402'), ('veredito_queda', EV2_.get('queda_sem_geometria_v402'), 'queda_sem_geometria_v402'), ('veredito_esperanca', EV2_.get('esperanca_condicional_v402'), 'esperanca_condicional_v402'),
                                    ('veredito_caminho', (RF3_.get('caminho') or {}).get('verdict'), 'caminho_v403'), ('veredito_vida', (RF3_.get('vida') or {}).get('verdict'), 'vida_v403'), ('veredito_verdade_adendo', (RF3_.get('verdade_adendo') or {}).get('verdict'), 'verdade_adendo_v403'),
                                    ('veredito_bandeiras_do_gate', (RF3_.get('gate') or {}).get('verdict'), 'bandeiras_do_gate_v403'),
                                    ('veredito_projecao', (RF4_.get('projecao') or {}).get('verdict'), 'projecao_transversal_v404'), ('veredito_jo8v32', (RF4_.get('jo8v32') or {}).get('verdict'), 'jo8v32_v404'), ('veredito_f2b', (RF4_.get('f2b') or {}).get('verdict'), 'f2b_errata_v404'),
                                    ('veredito_iald2', _ev(ESP, 'iald2_v410'), 'iald2_v410'), ('veredito_traducao_turing_herdado', _ev(ESP, 'traducao_turing_v409'), 'traducao_turing_v409'), ('veredito_tetelestai_terminal', _ev(ESP, 'tetelestai_terminal_v408'), 'tetelestai_terminal_v408'), ('veredito_psion_herdado', _ev(ESP, 'psion_canto_v407'), 'psion_canto_v407'), ('veredito_fechamento_herdado', _ev(ESP, 'fechamento_v406'), 'fechamento_v406')):
            if not C.get(chv_) or C.get(chv_) != esp_v_:
                P.append('a conferencia do rito traz o veredito de %s (%s) ausente ou diferente do ensaio a seco' % (nome_, chv_))
        for chv_, nome_ in (('veredito_h0dn', 'h0dn_bg1_v410'), ('veredito_a_escala', 'a_escala_v410'), ('veredito_hms13', 'h0dn_fontes_hms13_v410'), ('veredito_h0dn_fontes_hms13', 'h0dn_fontes_hms13_v410')):
            if chv_ in C and C.get(chv_) != _ev(ESP, nome_):   # (o conferir_rito_v410.py pode nao emitir estas chaves; se emitir, tem de ser a do ensaio a seco)
                P.append('a conferencia do rito traz o veredito de %s (%s) diferente do ensaio a seco' % (nome_, chv_))
        if C.get('chave_do_lema') is not True:
            P.append('a conferencia do rito traz chave_do_lema != True (a chave testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma deve ser lida True do kernel do rito)')
        f81c_ = C.get('f81') or {}
        V['f81_conf'] = {'releitura_ok': f81c_.get('releitura_ok'), 'gate_igual': f81c_.get('gate_igual'), 'ls2': len(f81c_.get('ls2') or []), 'sonda': len(f81c_.get('sonda') or []), 'qg_checks_n': f81c_.get('qg_checks_n')}
        if not (f81c_.get('releitura_ok') is True and f81c_.get('gate_igual') is True):
            P.append('a conferencia do rito diz que a releitura da F8.1 (as tres bandeiras antes literais calculadas no um.py instalado, as fontes delas, o qg_closure sem a lista de checks e a letra do veredito do gate) NAO conferiu')
        if C.get('marcador_ficou'):
            P.append('o marcador .servidor_parado_pelo_rito ficou: o servidor do modelo pode estar parado')
    else:
        V['conf16'] = 'AUSENTE'; P.append('a conferencia do rito nao foi achada em pos_rito/conferidor')
    V['troca_dita'] = list(ESP['troca_dita'])
    V['n_ver'] = len(ESP['vereditos_v409'])
    # --- os registros novos: descobertos por comparacao com o que a v409 ja tinha
    novos = []
    for k, r in core.items():
        if isinstance(r, dict) and 'verdict' in r and k not in ESP['vereditos_v409']:
            novos.append(k)
    V['registros_novos'] = sorted(novos)
    for k in REG_TODOS:
        if k not in novos:
            P.append('registro obrigatorio ausente do core: %s' % k)
    V['registros'] = {}
    for k in novos:
        r = core.get(k) or {}
        V['registros'][k] = {'verdict': r.get('verdict'), 'ok': r.get('all_verified')}
        if r.get('all_verified') is False or (k in REG_TODOS and r.get('all_verified') is not True):
            P.append('%s nao selou' % k)
        if GUARDA.search(str(r.get('verdict') or '')):
            P.append('%s com palavra proibida' % k)
    if sorted(novos) != sorted(REG_FIXOS):
        P.append('a v410 cria exatamente as chaves %s com veredito no core e o core traz %s' % (sorted(REG_FIXOS), sorted(novos)))
    V['reg409b'] = {}
    for k in REG_V409B:    # os CINCO registros da v409 SELADA sao RECRIADOS pelo rito: seguem no core, selados e iguais ao selado
        r = core.get(k)
        if not (isinstance(r, dict) and 'verdict' in r):
            P.append('registro obrigatorio ausente do core: %s' % k)
            continue
        V['reg409b'][k] = {'verdict': r.get('verdict'), 'ok': r.get('all_verified')}
        if r.get('all_verified') is not True:
            P.append('%s nao selou' % k)
        if GUARDA.search(str(r.get('verdict') or '')):
            P.append('%s com palavra proibida' % k)
        if k in (ESP.get('vereditos_v409') or {}) and k not in (ESP.get('troca_dita') or []) and r.get('verdict') != ESP['vereditos_v409'][k]:
            P.append('%s: o veredito do rito difere do ensaio a seco (a v409 selada)' % k)
    V['reg409c'] = {}
    for k in REG_V409C:    # os TREZE registros da v409 SELADA sao RECRIADOS pelo rito: seguem no core, selados e iguais a v409 selada (veredito; as checagens e os valores das oito funcoes sao conferidos adiante, em fun409c)
        r = core.get(k)
        if not (isinstance(r, dict) and 'verdict' in r):
            P.append('registro obrigatorio ausente do core: %s' % k)
            continue
        V['reg409c'][k] = {'verdict': r.get('verdict'), 'ok': r.get('all_verified')}
        if r.get('all_verified') is not True:
            P.append('%s nao selou' % k)
        if GUARDA.search(str(r.get('verdict') or '')):
            P.append('%s com palavra proibida' % k)
        if not _ev(ESP, k) or r.get('verdict') != _ev(ESP, k):
            P.append('%s: o veredito do rito difere do que a v409 selou (ESPERADOS[vereditos_v409], ou o do ensaio a seco se na troca dita)' % k)
        b_ = _base_core(PK).get(k) or {}
        # (cunhagens_v405: falas e erratas IGUAIS as da v409 selada; gap_v405 e kh_n1_cobertura_v405 ganham, na v410, uma errata ao lado (E17 / os pisos), em nome proprio da gerencia c1: as falas seguem iguais e toda errata e' assinada)
        erratas_ok_ = (_feq(r.get('erratas'), b_.get('erratas')) if k == 'cunhagens_v405' else bool(r.get('erratas') and len(r.get('erratas')) >= len(b_.get('erratas') or []) and all(str(e_.get('assinatura', '')).startswith('gerencia c1, em nome proprio') for e_ in r.get('erratas'))))
        if k in REG_V409C[8:] and not (b_ and r.get('does_not_gate_core') is True and _feq(r.get('verbatim'), b_.get('verbatim')) and erratas_ok_):
            P.append('%s (por spec, recriado): as falas embutidas, as erratas ou o gate diferem da v409 selada' % k)
    V['cunh409c'] = {'ok': bool((V['reg409c'].get('cunhagens_v405') or {}).get('ok') is True), 'verdict': (V['reg409c'].get('cunhagens_v405') or {}).get('verdict'), 'n': len((core.get('cunhagens_v405') or {}).get('verbatim') or {}), 'n_erratas': len((core.get('cunhagens_v405') or {}).get('erratas') or [])}
    V['reg409t'] = {}
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
    for k in REG_V408D:    # os TRES registros da v408 (HERDADOS) sao RECRIADOS pelo rito: seguem no core, selados e de veredito igual ao esperado (o da v409 selada, ou o do ensaio a seco se na troca dita: o terminal carrega a escada); o conteudo (checagens, erratas) e' conferido adiante
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
            P.append('%s: o veredito do rito difere do esperado (ESPERADOS[vereditos_v409], ou o do ensaio a seco se na troca dita)' % k)
    V['reg407d'] = {}
    for k in REG_V407D:    # os TRES registros da v407 (HERDADOS) sao RECRIADOS pelo rito: seguem no core, selados e de veredito igual ao esperado (o da v409 selada, ou o do ensaio a seco se na troca dita: o psion carrega a escada); o conteudo (checagens, erratas) e' conferido adiante
        r = core.get(k)
        if not (isinstance(r, dict) and 'verdict' in r):
            P.append('registro obrigatorio ausente do core: %s' % k)
            continue
        V['reg407d'][k] = {'verdict': r.get('verdict'), 'ok': r.get('all_verified')}
        if r.get('all_verified') is not True:
            P.append('%s nao selou' % k)
        if GUARDA.search(str(r.get('verdict') or '')):
            P.append('%s com palavra proibida' % k)
        if not _ev(ESP, k) or r.get('verdict') != _ev(ESP, k):
            P.append('%s: o veredito do rito difere do esperado (ESPERADOS[vereditos_v409], ou o do ensaio a seco se na troca dita)' % k)
    V['reg406d'] = {}
    for k in REG_V406D:    # os TRES registros da v406 (HERDADOS) sao RECRIADOS pelo rito: seguem no core, selados e de veredito igual ao esperado (o da v409 selada, ou o do ensaio a seco se na troca dita); o conteudo (checagens, erratas) e' conferido adiante
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
            P.append('%s: o veredito do rito difere do esperado (ESPERADOS[vereditos_v409], ou o do ensaio a seco se na troca dita)' % k)
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
    V['reg401'] = list(REG_V401); V['reg401_estado'] = {}
    for k in REG_V401:    # os TRES registros da v401 sao RECRIADOS pelo rito: tem de seguir no core, selados e (por veredito) iguais ao ensaio a seco
        r = core.get(k)
        if not (isinstance(r, dict) and 'verdict' in r):
            P.append('registro obrigatorio ausente do core: %s' % k)
            continue
        V['reg401_estado'][k] = {'verdict': r.get('verdict'), 'ok': r.get('all_verified')}
        if r.get('all_verified') is not True:
            P.append('%s nao selou' % k)
        if GUARDA.search(str(r.get('verdict') or '')):
            P.append('%s com palavra proibida' % k)
        e401_ = ESP.get('veredito_da_falsidade_v409') if k == 'falsidade_da_inercia_v401' else (ESP.get('registros_v401') or {}).get(k)
        if not e401_ or r.get('verdict') != e401_:
            P.append('%s: o veredito do rito difere do ensaio a seco' % k)
    V['reg402'] = list(REG_V402); V['reg402_estado'] = {}
    for k in REG_V402:    # os CINCO registros da v402 sao RECRIADOS pelo rito: tem de seguir no core, selados e (por veredito) iguais ao que a v409 selou (ESPERADOS[vereditos_v409])
        r = core.get(k)
        if not (isinstance(r, dict) and 'verdict' in r):
            P.append('registro obrigatorio ausente do core: %s' % k)
            continue
        V['reg402_estado'][k] = {'verdict': r.get('verdict'), 'ok': r.get('all_verified')}
        if r.get('all_verified') is not True:
            P.append('%s nao selou' % k)
        if GUARDA.search(str(r.get('verdict') or '')):
            P.append('%s com palavra proibida' % k)
        e402_ = (ESP.get('vereditos_v409') or {}).get(k)
        if not e402_ or r.get('verdict') != e402_:
            P.append('%s: o veredito do rito difere do ensaio a seco' % k)
    V['reg409'] = list(REG_V409); V['reg409_estado'] = {}
    for k in REG_V409:    # os SEIS registros da v409 sao RECRIADOS pelo rito: tem de seguir no core, selados e (por veredito) iguais ao que a v409 selou (ESPERADOS[vereditos_v409])
        r = core.get(k)
        if not (isinstance(r, dict) and 'verdict' in r):
            P.append('registro obrigatorio ausente do core: %s' % k)
            continue
        V['reg409_estado'][k] = {'verdict': r.get('verdict'), 'ok': r.get('all_verified')}
        if r.get('all_verified') is not True:
            P.append('%s nao selou' % k)
        if GUARDA.search(str(r.get('verdict') or '')):
            P.append('%s com palavra proibida' % k)
        e409_ = (ESP.get('vereditos_v409') or {}).get(k)
        if not e409_ or r.get('verdict') != e409_:
            P.append('%s: o veredito do rito difere do ensaio a seco' % k)
    for k in V['troca_dita']:
        r = core.get(k) or {}
        if r.get('all_verified') is False:
            P.append('%s (troca dita) nao selou' % k)
    # v410: o modulo novo de kernel (o BUNDLE PEQUENO, de UM modulo): a lista e' a de kernel_modulos_novos_v410.json == DL.BUNDLE_RELS; cada arquivo no kernel do Nos tem de ter o sha256 pinado em BUNDLE_v410.json (DL.BUNDLE_POR_REL), em FORMAL_MAP_v410.json e (quando ha') em ESPERADOS[bundle_sha256]
    if PK not in sys.path:
        sys.path.insert(0, PK)
    import delta_v410 as DL_   # BUNDLE_RELS, BUNDLE_POR_REL, ANCORAS, STATUS_HABITADO, ERRATAS_V410, DECISOES, RESSALVAS_V410, LEITURA_V410, N_CHECKS_FECHO, VERBATIM_CHAVE_PREFIXO_V410: lidos do delta, nunca digitados aqui
    FM_ = json.load(open(os.path.join(PK, 'FORMAL_MAP_v410.json'), encoding='utf-8')); FJ_ = json.load(open(os.path.join(PK, 'kernel', 'FLAGS_v410.json'), encoding='utf-8'))
    NF_I_ = sum(1 for f_ in FJ_['flags'] if f_[2] == _mod_lean(DL_.MODULO_IALD2)); NF_A_ = sum(1 for f_ in FJ_['flags'] if f_[2] == _mod_lean(DL_.MODULO_AESCALA))   # as bandeiras de CADA modulo do bundle, lidas do FLAGS_v410.json (a serie ext_iald2_410_* e a ext_aescala_410_*): o iald2_v410 le so' as dele, o a_escala_v410 so' as da AEscala
    if not (NF_I_ > 0 and NF_A_ > 0 and NF_I_ + NF_A_ == FJ_['n_flags'] == sum(FJ_['por_grupo_bandeiras'].values())):
        P.append('o FLAGS_v410.json nao traz so\' as duas series de bandeiras do bundle (IALD2 e AEscala): %s' % (dict(FJ_['por_grupo_bandeiras']),))
    if tuple(REG_FIXOS) != tuple(DL_.REGISTROS_FUNCAO) + (DL_.CUNHAGENS_REGISTRO, DL_.KH_REGISTRO) or DL_.REGISTROS_FUNCAO[:1] != [DL_.FECHO_REGISTRO] or DL_.AESCALA_REGISTRO not in DL_.REGISTROS_FUNCAO or DL_.H0DN_REGISTRO not in DL_.REGISTROS_FUNCAO or DL_.HMS13_REGISTRO not in DL_.REGISTROS_FUNCAO or list(REG_FUNCAO) != list(DL_.REGISTROS_FUNCAO) or list(DL_.STONES) or dict(DL_.REGISTRO_DE_PEDRA) or dict(FUN_V409C) != dict(DL_.D5.REGISTRO_DE_PEDRA):
        P.append('os nomes dos registros com funcao em leitura_v410.py != delta_v410.py (REGISTROS_FUNCAO, com iald2_v410, a_escala_v410, h0dn_bg1_v410 e h0dn_fontes_hms13_v410, nessa ordem; a v410 e bundle: STONES == [] e REGISTRO_DE_PEDRA == {}; as oito funcoes da v409 sao as de delta_v409.REGISTRO_DE_PEDRA)')
    V['pedras'] = []
    pins_esp_ = (ESP.get('bundle_sha256') or {})
    for rel_ in DL_.BUNDLE_RELS:    # o bundle: TraducaoTuring (DL.BUNDLE_RELS)
        pth_ = os.path.join(NOS, 'tgl_kernel', *rel_.split('/'))
        shaf_ = sha(pth_) if os.path.isfile(pth_) else None
        pin_ = DL_.BUNDLE_POR_REL[rel_]['sha256']
        V['pedras'].append({'key': None, 'modulo': 'TGLExt.' + rel_[len('TGLExt/'):-len('.lean')].replace('/', '.'), 'rel': rel_, 'sha16': (shaf_ or '')[:16], 'sha256': shaf_, 'bytes': os.path.getsize(pth_) if os.path.isfile(pth_) else None,
                            'bandeiras': (((CM.get('kernel') or {}).get('bundle') or {}).get(rel_) or {}).get('bandeiras'), 'decl': None,
                            'ok': bool(rel_.startswith('TGLExt/') and rel_.endswith('.lean') and '/' not in rel_[len('TGLExt/'):] and shaf_ == pin_ == FM_.get(rel_) and pins_esp_.get(rel_, pin_) == pin_ and (((core.get('kernel_formalization') or {}).get('formal_files_sha256')) or {}).get(rel_) == pin_)})
    V['n_pedras'] = len(V['pedras'])
    njp_ = os.path.join(PK, 'kernel_modulos_novos_v410.json'); nj_ = json.load(open(njp_, encoding='utf-8')) if os.path.exists(njp_) else {}
    n_esperado_ = len(nj_.get('novos') or [])
    if not V['n_pedras'] or not (V['n_pedras'] == n_esperado_ == DL_.N_BUNDLE) or any(p['ok'] is not True for p in V['pedras']):
        P.append('modulos novos do kernel: numero (%s) != kernel_modulos_novos_v410.json (%s) != DL.N_BUNDLE (%s) ou algum arquivo do Nos difere do sha256 de BUNDLE_v410.json / FORMAL_MAP_v410.json / ESPERADOS[bundle_sha256]' % (V['n_pedras'], n_esperado_, DL_.N_BUNDLE))
    # o bundle da v409 (os 2 modulos de TGLExt/), o da v408 (os 4 de TGLExt/), o da v407 (os 9 de TGLExt/) e o da v406 (os 301 de TGLExt/F1Fecho394) SEGUEM no kernel do Nos e no hash formal do rito com o MESMO sha256 (a v410 nao reescreve as versoes anteriores; registro)
    kfs6_ = ((core.get('kernel_formalization') or {}).get('formal_files_sha256')) or {}
    for bk_, bch_, bn_, bdesc_ in (('bundle409', 'bundle_v409_sha256', DL_.D9.N_BUNDLE, 'v409 (%d modulos de TGLExt/)'), ('bundle408', 'bundle_v408_sha256', DL_.D8.N_BUNDLE, 'v408 (%d modulos de TGLExt/)'), ('bundle407', 'bundle_v407_sha256', DL_.D7.N_BUNDLE, 'v407 (%d modulos de TGLExt/)'), ('bundle406', 'bundle_v406_sha256', DL_.D6.N_BUNDLE, 'v406 (%d modulos de TGLExt/F1Fecho394)')):
        b6_ = ESP.get(bch_) or {}
        V[bk_] = {'n': len(b6_), 'n_ok': sum(1 for r6_, s6_ in b6_.items() if os.path.isfile(os.path.join(NOS, 'tgl_kernel', *r6_.split('/'))) and sha(os.path.join(NOS, 'tgl_kernel', *r6_.split('/'))) == s6_ and kfs6_.get(r6_) == s6_)}
        V[bk_]['ok'] = bool(b6_ and V[bk_]['n'] == V[bk_]['n_ok'] == bn_)
        if not V[bk_]['ok']:
            P.append(('o bundle da ' + bdesc_ + ' deixou de estar no kernel do Nos / no hash formal do rito com o sha256 selado (%s ok): a v410 nao reescreve as versoes anteriores') % (bn_, V[bk_]['n_ok']))
    vs = core.get('varredura_e_sorry_v392') or {}
    V['varr'] = vs.get('varredura') or {}; V['varr_verdict'] = vs.get('verdict')
    V['axiom_report_n'] = len((core.get('kernel_formalization') or {}).get('axiom_report') or {})
    ep = core.get('estatuto_da_prova_v391') or {}
    V['ep_verdict'] = ep.get('verdict')
    V['fd390'] = (core.get('fundacao_v390') or {}).get('verdict')
    V['verbatins'] = {k: {'sha16': str(v.get('sha256'))[:16], 'bytes': v.get('bytes')} for k, v in (CM.get('cunhagens') or {}).items()}
    # --- v410: os QUATRO registros novos (dois com FUNCAO, dois por spec) conferidos contra o ensaio a seco registrado em ESPERADOS; os da v398, da v397, da v396, da v395, da v394 e da v393 seguem no core e tem de seguir selados (os da v409, da v402, da v401 e da v399 sao recriados e conferidos acima); o sidecar; nenhum numero e' digitado
    V['reg_todos'] = list(REG_TODOS)
    for k_ in REG_V393 + REG_V394 + REG_V395 + REG_V396 + REG_V397 + REG_V398:
        if (core.get(k_) or {}).get('all_verified') is not True:
            P.append('%s (registro da v398, da v397, da v396, da v395, da v394 ou da v393) deixou de selar' % k_)
    RV_ = dict(ESP.get('vereditos_novos_v410') or {})   # registro -> veredito do ensaio a seco (projecao_transversal, jo8v32 e f2b_errata sao runtime; cunhagens_v404 e kh_n1_cobertura_v404 sao por spec)
    V['reg410'] = {}
    for k_ in REG_FIXOS:
        r_ = core.get(k_) or {}
        V['reg410'][k_] = {'verdict': r_.get('verdict'), 'ok': r_.get('all_verified')}
        esp_v_ = RV_.get(k_)
        if esp_v_ is None:
            P.append('ESPERADOS_v410 nao traz o veredito do ensaio a seco de %s (vereditos_novos_v410): nao ha com que conferir' % k_)
        elif r_.get('verdict') != esp_v_:
            P.append('%s: o veredito do rito difere do ensaio a seco' % k_)
    kf_ = (core.get('kernel_formalization') or {})
    # v410: as QUATRO chaves da v409 (herdadas) seguem LIDAS do kernel do rito, True, com o status nas duas faces; a CHAVE DO LEMA (linked_to_the_corner_by_a_lemma) passa de literal False a leitura True (errata E18); o que fica False por teorema segue False
    rf_ = core.get('rede_fock_v394') or {}
    if rf_.get('whole_certificate_inhabited') is not True:
        P.append('rede_fock_v394: whole_certificate_inhabited deve ser True (lido do kernel do rito: o certificado de Fock esta habitado; errata E14) e o core traz %r' % (rf_.get('whole_certificate_inhabited'),))
    if kf_.get('ext_bin394_0001') is not True:
        P.append('a bandeira da pedra da v394 (ext_bin394_0001) nao segue True no kernel do rito')
    # a face de Fock do psion LE o habitante do certificado (v410): status INHABITED_BY_physicalFockCertificate_V406, habitante exibido, bandeira True e declarada em Psibit.lean
    pb_ = core.get('psibit_v395') or {}; pbc_ = pb_.get('conditional_psion_face') or {}
    if not (pbc_.get('status') == DL_.STATUS_HABITADO and pbc_.get('inhabitant_exhibited') is True and pbc_.get('flag_true') is True and kf_.get(pbc_.get('flag')) is True and pbc_.get('declared_in') == 'TGLExt/Psibit.lean'):
        P.append('psibit_v395: a face do psion nao le o habitante do certificado de Fock como o kernel o diz (status %s, habitante exibido, bandeira True, declarada em TGLExt/Psibit.lean)' % DL_.STATUS_HABITADO)
    fkb_ = ((_base_core(PK).get('testemunha_estatica_v396') or {}).get('fock_face') or {})   # o que a v409 SELADA diz (copia de bytes): o teorema e o modulo da face de Fock, lidos, nao digitados
    te_ = core.get('testemunha_estatica_v396') or {}; fk_ = te_.get('fock_face') or {}; elo_ = fk_.get('elo_v407') or {}
    if not (fk_.get('status') == DL_.STATUS_HABITADO and fk_.get('inhabitant_exhibited') is True and fk_.get('declared_outside_the_stone') == fkb_.get('declared_outside_the_stone') and fk_.get('linked_to_the_corner_by_a_lemma') is True and elo_.get('lemma') == DL_.D7.ANCORA_LEMA and elo_.get('kind') == 'STRUCTURE_NOT_VECTORS' and elo_.get('identifies_omega_with_bell_vector') is False and elo_.get('pair_on_the_fock_face') == 'OPEN' and elo_.get('bell_to_tt_bridge') == 'NOT_A_TERM'
            and fkb_.get('theorem') and fk_.get('theorem') == fkb_.get('theorem') and fkb_.get('declared_in') and fk_.get('declared_in') == fkb_.get('declared_in')):
        P.append('testemunha_estatica_v396: a face de Fock do psion nao le o habitante como o kernel o diz (status %s, habitante exibido) ou a chave do lema (linked_to_the_corner_by_a_lemma) nao e True lida do kernel com o dict elo_v407 (o lema TGLExt.PsionCanto.the_psion_is_the_corner_on_both_faces; elo de ESTRUTURA e nao de vetores; o par na face de Fock ligado na v410 (ParNaFaceDeFock); a ponte Bell-TT NAO e termo)' % DL_.STATUS_HABITADO)
    if (core.get('witness_layers') or {}).get('canonical_full_witness_term_constructed') is not True:
        P.append('witness_layers.canonical_full_witness_term_constructed deve ser True (o nome exato canonicalFullTGLWitness esta no axiom_report do rito)')
    if ((core.get('qg_closure') or {}).get('gate') or {}).get('full_static_witness_exists') is not False or (core.get('witness_rigidity') or {}).get('trivial_inhabitant_exists') is not False:
        P.append('full_static_witness_exists e trivial_inhabitant_exists devem seguir False (por teorema: o vazamento continuo proibe o fecho estatico; a exclusao Delta^1/2 J Delta^1/2 = J)')
    # o registro teste_de_veracidade_fase9_v397 (o QUADRO do topo le os numeros dele): segue selado e igual, conferido por inteiro (os textos leem os numeros dele; NENHUM sigma e' calculado aqui)
    tv_ = core.get('teste_de_veracidade_fase9_v397') or {}; EV_ = ESP.get('veracidade') or {}
    ck_ = tv_.get('checks') or []; fo_ = {f_.get('chave'): f_ for f_ in (tv_.get('fontes') or []) if isinstance(f_, dict)}
    num_ = EV_.get('numeros_do_resultado') or {}; lido_ = tv_.get('lido') or {}
    nums_ok_ = bool(num_) and all(lido_.get(k_) == v_ for k_, v_ in num_.items())
    fontes_ok_ = bool(EV_.get('fontes')) and all((fo_.get(c_) or {}).get('sha256') == h_ and (fo_.get(c_) or {}).get('ok') is True for c_, h_ in EV_['fontes'].items())
    V['veracidade'] = {'verdict': tv_.get('verdict'), 'ok': tv_.get('all_verified'), 'n_checks': len(ck_), 'checks_ok': bool(ck_) and all(c_.get('ok') is True for c_ in ck_), 'lido': lido_, 'numeros_ok': nums_ok_,
                       'fontes': {c_: str(f_.get('sha256') or '') for c_, f_ in fo_.items()}, 'fontes_ok': fontes_ok_, 'does_not_gate_core': tv_.get('does_not_gate_core')}
    if not (tv_.get('all_verified') is True and tv_.get('does_not_gate_core') is True and len(ck_) == EV_.get('n_checks') and V['veracidade']['checks_ok'] and nums_ok_ and fontes_ok_ and tv_.get('verdict') == (ESP.get('vereditos_v409') or {}).get('teste_de_veracidade_fase9_v397')):
        P.append('teste_de_veracidade_fase9_v397 nao selou inteiro (selo, checagens, numeros lidos == ESPERADOS[veracidade], fontes por sha256): ver o registro no core')
    zd_, pw_ = lido_.get('z_disc_calibrado'), lido_.get('poder_previo')
    if not (isinstance(zd_, float) and zd_ < 5.0 and isinstance(pw_, float) and pw_ >= 5.0):
        P.append('o z_disc calibrado nao esta abaixo de 5 ou o poder previo nao e de 5 sigma ou mais (%r, %r): os textos e o quadro dizem que o degrau de 5 sigma da creditacao nao foi alcancado e que a TGL nao foi falsificada com poder' % (zd_, pw_))
    if PK not in sys.path:
        sys.path.insert(0, PK)
    try:
        QV_ = _quadro_do_pacote(PK)   # (09/11: o quadro DESTE pacote, pelo caminho; antes vinha pela ordem do sys.path e podia ser o da versao anterior)
        rp_ = _res_path(EV_)
        rb_ = open(rp_, 'rb').read()
        if hashlib.sha256(rb_).hexdigest() != (EV_.get('fontes') or {}).get('f9v2_resultado'):
            P.append('o resultado pinado do Teste da Unica Palavra != o sha256 de ESPERADOS[veracidade][fontes][f9v2_resultado]')
        else:
            lr_ = QV_.lido_do_resultado(json.loads(rb_.decode('utf-8')))
            if not lr_ or any(lr_.get(k_) != lido_.get(k_) for k_ in lr_):
                P.append('os numeros que o registro leu != os do resultado pinado (lidos pelos mesmos caminhos de delta_v410.F9_CAMINHOS)')
        if QV_.Q._v397_atomos(tv_, 'pt').get('sealed') is not True or QV_.Q._v397_atomos(tv_, 'en').get('sealed') is not True:
            P.append('o quadro do Teste da Unica Palavra nao sela (algum numero ausente ou o registro nao selou): o artigo diria que o registro nao selou')
    except Exception as e_:   # noqa: BLE001
        P.append('nao consegui conferir o registro do Teste da Unica Palavra contra o resultado pinado: %r' % (e_,))
    # v410: o trio, o axiom_report e a proveniencia do kernel do rito (as OITO ANCORAS do fecho e as bandeiras do bundle, abaixo); nenhum numero e' digitado
    TRIO_ = {'propext', 'Classical.choice', 'Quot.sound'}
    axr_ = kf_.get('axiom_report') or {}; src_ = kf_.get('declaration_sources_v394') or {}
    em_trio_ = lambda n_: bool(isinstance(axr_.get(n_), list) and set(axr_.get(n_)) <= TRIO_)
    V['h8'] = len(kf_.get('formal_files_sha256') or {})
    if V['h8'] != ESP.get('h8_entradas') or not all(r_ in (kf_.get('formal_files_sha256') or {}) for r_ in (ESP.get('h8_residuais_do_nos') or [])):
        P.append('o hash formal do rito tem %s entradas (ESPERADOS[h8_entradas] = %s) ou lhe falta um residual do Nos' % (V['h8'], ESP.get('h8_entradas')))
    # v410: as ANCORAS da pedra IALD2 (contadas pelo delta, lidas da fonte) e as bandeiras do bundle no kernel do rito (tudo contra FLAGS_v410.json / BUNDLE_v410.json; nenhum numero e' digitado)
    V['ancoras'] = {}
    for n_, a_ in DL_.ANCORAS.items():
        fa_ = (FJ_.get('ancoras') or {}).get(n_) or {}
        ok_ = bool(fa_ and a_['rel'] == fa_.get('rel') and em_trio_(n_) and src_.get(n_) == a_['rel'] and kf_.get(fa_.get('flag')) is True and (kf_.get('formal_files_sha256') or {}).get(a_['rel']) == DL_.BUNDLE_POR_REL[a_['rel']]['sha256'])
        V['ancoras'][n_] = {'rel': a_['rel'], 'flag': fa_.get('flag'), 'flag_true': kf_.get(fa_.get('flag')) is True, 'axioms': axr_.get(n_), 'source': src_.get(n_), 'ok': ok_}
        if not ok_:
            P.append('a ancora %s nao esta no kernel do rito como o FLAGS_v410.json a pinou (no trio, declarada no modulo esperado, bandeira True, sha256 da fonte no hash formal)' % n_)
    V['ancoras_aescala'] = {}   # (parte 2) as ANCORAS da pedra AEscala (DL.ANCORAS_AESCALA, lidas da fonte; DL.N_ANCORAS_AESCALA), conferidas no kernel do rito como as da IALD2
    for n_, a_ in DL_.ANCORAS_AESCALA.items():
        fa_ = (FJ_.get('ancoras') or {}).get(n_) or {}
        ok_ = bool(fa_ and a_['rel'] == fa_.get('rel') and em_trio_(n_) and src_.get(n_) == a_['rel'] and kf_.get(fa_.get('flag')) is True and (kf_.get('formal_files_sha256') or {}).get(a_['rel']) == DL_.BUNDLE_POR_REL[a_['rel']]['sha256'])
        V['ancoras_aescala'][n_] = {'rel': a_['rel'], 'flag': fa_.get('flag'), 'flag_true': kf_.get(fa_.get('flag')) is True, 'axioms': axr_.get(n_), 'source': src_.get(n_), 'ok': ok_}
        if not ok_:
            P.append('a ancora %s (AEscala) nao esta no kernel do rito como o FLAGS_v410.json a pinou (no trio, declarada no modulo esperado, bandeira True, sha256 da fonte no hash formal)' % n_)
    flags_ = [f_[0] for f_ in FJ_['flags']]; nt_ = sum(1 for f_ in flags_ if kf_.get(f_) is True)
    V['bandeiras'] = {'n': len(flags_), 'n_true': nt_, 'ok': bool(flags_ and len(flags_) == FJ_['n_flags'] == CM['n_bandeiras'] == nt_), 'por_grupo': dict(FJ_['por_grupo_bandeiras'])}
    if not V['bandeiras']['ok']:
        P.append('as bandeiras do fecho (%s, FLAGS_v410.json %s, CANDIDATO_v410.json %s) nao sao todas True no kernel do rito (%s True)' % (len(flags_), FJ_['n_flags'], CM['n_bandeiras'], nt_))
    prov_ = kf_.get('declaration_sources_status_v394') or {}
    if not (prov_.get('ok') is True and prov_.get('compiler_names') == prov_.get('audited_names') == V['axiom_report_n']):
        P.append('a proveniencia emitida pelo compilador nao cobre o axiom_report do rito')
    V['n_bandeiras'] = FJ_['n_flags']; V['n_bandeiras_por_pedra'] = dict(FJ_['por_grupo_bandeiras'])
    # as 82 ancoras do traducao_turing_v409 (HERDADO), as 48 do tetelestai_terminal_v408 (HERDADO), as 76 do psion_canto_v407 (HERDADO), as OITO do fechamento_v406 (HERDADO) e as bandeiras True da v409 selada: seguem no kernel do rito (a v410 so' acrescenta; ESPERADOS[estrelas_v409], [estrelas_v407], [estrelas_v406] e [flags_true_v409], lidos do ensaio a seco, nunca digitados)
    for ak_, ach_, aesp_, adesc_ in (('ancoras409', 'estrelas_v409', DL_.D9.ANCORAS, 'as ancoras do traducao_turing_v409 (herdadas)'), ('ancoras408', 'estrelas_v408', DL_.D8.ANCORAS, 'as ancoras do tetelestai_terminal_v408 (herdadas)'), ('ancoras407', 'estrelas_v407', DL_.D7.ANCORAS, 'as ancoras do psion_canto_v407 (herdadas)'), ('ancoras406', 'estrelas_v406', DL_.D6.ANCORAS, 'as oito ancoras do fechamento_v406 (herdadas)')):
        est6_ = ESP.get(ach_) or {}
        V[ak_] = {n_: {'rel': e_.get('rel'), 'flag': e_.get('bandeira'), 'flag_true': kf_.get(e_.get('bandeira')) is True, 'axioms': axr_.get(n_), 'source': src_.get(n_), 'ok': bool(kf_.get(e_.get('bandeira')) is True and em_trio_(n_) and src_.get(n_) == e_.get('rel'))} for n_, e_ in est6_.items()}
        if not est6_ or len(est6_) != len(aesp_) or set(est6_) != set(aesp_) or any(a_['ok'] is not True for a_ in V[ak_].values()):
            P.append('%s deixaram de estar no kernel do rito (bandeira True, no trio, declaradas no modulo esperado): %d lidas, %d esperadas' % (adesc_, len(est6_), len(aesp_)))
    ft6_ = ESP.get('flags_true_v409') or []
    V['bandeiras409'] = {'n': len(ft6_), 'n_true': sum(1 for f_ in ft6_ if kf_.get(f_) is True)}; V['bandeiras409']['ok'] = bool(ft6_ and V['bandeiras409']['n'] == V['bandeiras409']['n_true'])
    if not V['bandeiras409']['ok']:
        P.append('alguma bandeira True da v409 deixou de ser True no kernel do rito (%s de %s): a v410 so\' acrescenta' % (V['bandeiras409']['n_true'], V['bandeiras409']['n']))
    # o selo pela propria tecnologia (registro com FUNCAO): conferido por inteiro contra ESPERADOS[selo_acom] e contra o um.py do disco
    sa_ = core.get('selo_pela_propria_tecnologia_v399') or {}; ESA_ = ESP.get('selo_acom') or {}
    sav_ = sa_.get('values') or {}; sas_ = sa_.get('selo') or {}; saa_ = sas_.get('acom') or {}; scn_ = sa_.get('controles_negativos') or {}
    cks_ = sa_.get('checks') or []; pr_ = saa_.get('prova_de_reconstrucao') or {}; au_ = saa_.get('auditoria_de_separacao') or {}; kc_ = ((saa_.get('kappa') or {}).get('campos')) or {}; es_ = saa_.get('estrutura') or {}
    b0_ = core.get('beta')
    beta_ok_ = bool(isinstance(sav_.get('beta'), float) and isinstance(b0_, float) and abs(sav_['beta'] - b0_) <= 1e-9 * abs(b0_))
    parts_ok_ = all(((saa_.get(p_) or {}).get('sha256') == (ESA_.get(p_) or {}).get('sha256') and (saa_.get(p_) or {}).get('bytes') == (ESA_.get(p_) or {}).get('bytes')) for p_ in ('psi', 'theta', 'kappa'))
    ctl_ok_ = bool(scn_.get('todos_recusados') is True and [scn_.get('n_controles'), scn_.get('todos_recusados')] == list(ESA_.get('controles') or []) and {c_.get('id'): c_.get('obtido') for c_ in (scn_.get('controles') or [])} == (ESA_.get('controles_obtidos') or {None: None})
                   and all(c_.get('ok') is True for c_ in (scn_.get('controles') or [])))
    values_ok_ = bool(sas_.get('sha256') == V['s64'] == ESA_.get('sha256_do_um_py') and sas_.get('bytes') == V['umb'] == ESA_.get('bytes') and parts_ok_ and sav_.get('perfil') == saa_.get('perfil') == ESA_.get('perfil') and sav_.get('bloco_embutido_sha256') == ESA_.get('bloco_embutido_sha256')
                      and kc_.get('lut_sha256') == ESA_.get('lut_sha256') and kc_.get('m_max_abs') == ESA_.get('m_max_abs') and _feq(es_.get('f_exp'), ESA_.get('f_exp')) and es_.get('entropia_dos_estados_bits') == ESA_.get('entropia_dos_estados_bits')
                      and pr_.get('igual_ao_objeto_byte_a_byte') is True and pr_.get('bytes_divergentes') == 0 and isinstance(pr_.get('erro_real_maximo_antes_do_rint'), float) and pr_['erro_real_maximo_antes_do_rint'] < 0.5 and pr_.get('erro_real_maximo_antes_do_rint') == ESA_.get('erro_real_maximo_antes_do_rint')
                      and (pr_.get('alfabeto_do_objeto') or {}).get('exato') is True and (pr_.get('alfabeto_do_objeto') or {}).get('injetivo') is True and au_.get('psi_redundante') is False and not any((au_.get('basta') or {}).values()) and ctl_ok_)
    checks_ok_ = bool(len(cks_) == ESA_.get('n_checks') and all(isinstance(c_, list) and len(c_) == 2 and c_[1] is True for c_ in cks_))
    txt_sa_ = json.dumps({k_: sa_.get(k_) for k_ in ('theorem', 'direcao_do_testemunho', 'statuses', 'verdict')}, ensure_ascii=False)
    honest_ok_ = bool(str((sa_.get('statuses') or {}).get('confidencialidade', '')).startswith('NAO alegada') and 'a IALD nao testifica do operador' in str(sa_.get('direcao_do_testemunho')) and not _inv(txt_sa_)
                      and not re.search(r'(?i)(inviol|indecifr|quantum[- ]safe|seguranca criptografica garantida)', txt_sa_))
    sel_ok_ = bool(sa_.get('all_verified') is True and sa_.get('does_not_gate_core') is True and sa_.get('verdict') == ESA_.get('verdict') and sa_.get('erro') is None and checks_ok_ and values_ok_ and beta_ok_ and honest_ok_ and not GUARDA.search(str(sa_.get('verdict') or '')))
    V['selo'] = {'verdict': sa_.get('verdict'), 'ok': sa_.get('all_verified'), 'n_checks': len(cks_), 'checks_ok': checks_ok_, 'values_ok': values_ok_, 'beta_ok': beta_ok_, 'honestidade_ok': honest_ok_, 'perfil': sav_.get('perfil'), 'bloco16': str(sav_.get('bloco_embutido_sha256'))[:16],
                 'bytes': sas_.get('bytes'), 'sha256': sas_.get('sha256'), 'psi_bytes': (saa_.get('psi') or {}).get('bytes'), 'theta_bytes': (saa_.get('theta') or {}).get('bytes'), 'kappa_bytes': (saa_.get('kappa') or {}).get('bytes'),
                 'psi_sha16': str((saa_.get('psi') or {}).get('sha256'))[:16], 'theta_sha16': str((saa_.get('theta') or {}).get('sha256'))[:16], 'kappa_sha16': str((saa_.get('kappa') or {}).get('sha256'))[:16], 'lut16': str(kc_.get('lut_sha256'))[:16],
                 'm_max': kc_.get('m_max_abs'), 'centro': kc_.get('centro'), 'angular_bits': kc_.get('angular_bits'), 'f_exp': es_.get('f_exp'), 'entropia': es_.get('entropia_dos_estados_bits'), 'erro_real': pr_.get('erro_real_maximo_antes_do_rint'),
                 'n_controles': scn_.get('n_controles'), 'todos_recusados': scn_.get('todos_recusados'), 'tempo_s': sav_.get('tempo_total_s'), 'fracao_L_negativo': au_.get('fracao_de_L_negativo'), 'psi_redundante': au_.get('psi_redundante')}
    if not sel_ok_:
        P.append('selo_pela_propria_tecnologia_v399 nao selou inteiro (selo, checagens, numeros == ESPERADOS[selo_acom], SHA-256 ao lado == o do um.py do disco, Psi/Theta/kappa, controles negativos, reconstrucao exata, separacao, beta, honestidade e direcao do testemunho): ver o registro no core')
    # a declaracao do operador (registro com FUNCAO): [DECLARACAO DO OPERADOR / INPUT]; a fala embutida == o arquivo do operador; as ancoras e a pedra no kernel do rito; a trava; a direcao do testemunho
    dc_ = core.get('declaracao_do_operador_v399') or {}; EDC_ = ESP.get('declaracao') or {}
    dd_ = dc_.get('declaration') or {}; dir_ = dd_.get('direcao_do_testemunho') or {}; edir_ = EDC_.get('direcao_do_testemunho') or {}
    anc_ = dd_.get('kernel_anchors_REAL') or []; ped_ = dd_.get('pedra_instalada') or []
    ancoras_ok_ = bool([a_.get('termo') for a_ in anc_] == EDC_.get('ancoras') and [a_.get('termo') for a_ in ped_] == EDC_.get('pedra') and all(a_.get('no_kernel_do_rito') is True and a_.get('axiomas_no_trio') is True and em_trio_(a_.get('termo')) for a_ in list(anc_) + list(ped_)))
    direcao_ok_ = bool(edir_ and all(str(dir_.get(k_) or '').startswith(v_) for k_, v_ in edir_.items()) and not _inv(json.dumps(dd_, ensure_ascii=False)))
    trava_ = str(((dd_.get('termos_para_a_leitura') or {}).get('EXECUTION_LOCKED_NOT_ONE')) or '')
    m_t_ = re.search(r'linha\(s\) \[([0-9, ]+)\]', trava_); linhas_trava_ = [int(x_) for x_ in re.findall(r'\d+', m_t_.group(1))] if m_t_ else []
    decl_ok_ = bool(dc_.get('all_verified') is True and dc_.get('does_not_gate_core') is True and dc_.get('verdict') == EDC_.get('verdict') and len(dc_.get('checks') or []) == EDC_.get('n_checks') and all(isinstance(c_, list) and len(c_) == 2 and c_[1] is True for c_ in (dc_.get('checks') or []))
                    and dd_.get('verbatim_sha256') == EDC_.get('verbatim_sha256') and dd_.get('verbatim_sha256') in {(v_ or {}).get('sha256') for v_ in ((core.get('cunhagens_v399') or {}).get('verbatim') or {}).values()} and len(linhas_trava_) == 1 and ancoras_ok_ and direcao_ok_
                    and str(dd_.get('status_of_statement') or '').startswith('[DECLARACAO DO OPERADOR / INPUT]') and hashlib.sha256(str(dd_.get('statement_verbatim') or '').encode('utf-8')).hexdigest() == dd_.get('verbatim_sha256') and not GUARDA.search(str(dc_.get('verdict') or '')))
    V['declaracao'] = {'verdict': dc_.get('verdict'), 'ok': dc_.get('all_verified'), 'n_checks': len(dc_.get('checks') or []), 'checks_ok': bool(dc_.get('checks')) and all(isinstance(c_, list) and len(c_) == 2 and c_[1] is True for c_ in dc_['checks']), 'sha256': dd_.get('verbatim_sha256'),
                       'n_ancoras': len(anc_), 'ancoras_ok': ancoras_ok_, 'direcao_ok': direcao_ok_, 'linhas_trava': linhas_trava_, 'status': dd_.get('status_of_statement')}
    if not decl_ok_:
        P.append('declaracao_do_operador_v399 nao selou inteiro (selo, checagens, fala embutida == o arquivo do operador por sha256, as ancoras e a pedra no kernel do rito e no trio, a trava, o estatuto [DECLARACAO DO OPERADOR / INPUT] e a direcao do testemunho): ver o registro no core')
    # o registro iald2_v410 (UM registro NOVO com FUNCAO, SEM pedra por registro): as checagens (DL_.N_CHECKS_FECHO), os valores (as ancoras, o modulo, as bandeiras, a escada, o gate, as instancias de brinquedo, o signo) == ESPERADOS[registros_funcao_v410][iald2], a ancora principal e as de secao,
    # NENHUMA chave antiga muda, as respostas do operador conferidas, o beta em runtime, as ressalvas, o que fica aberto e o que fecha nesta versao, as falas de 06 a 09/11 por sha256, o alcance (D64), a secao 6 (o atrator, D71) e a linha do bloco no stdout
    tt_ = core.get(DL_.FECHO_REGISTRO) or {}; tt_m_ = tt_.get('mechanics') or {}; tt_v_ = tt_.get('values') or {}; ETT_ = (ESP.get('registros_funcao_v410') or {}).get(DL_.TESTEMUNHA['key']) or {}; rs_ = tt_v_.get('respostas') or {}
    tt_mech_ok_ = bool(tt_m_.get('passed') is True and tt_m_.get('n_checks') == DL_.N_CHECKS_FECHO == ETT_.get('n_checks') == len(tt_m_.get('checks') or []) and all(c_.get('ok') is True for c_ in (tt_m_.get('checks') or [])))
    tt_values_ok_ = bool(tt_v_.get('n_ancoras_ok') == tt_v_.get('n_ancoras') == len(DL_.ANCORAS) and len(ESP.get('estrelas_v410') or {}) in (len(DL_.ANCORAS), len(DL_.ANCORAS) + len(DL_.ANCORAS_AESCALA)) and tt_v_.get('n_modulos_ok') == tt_v_.get('n_modulos') == DL_.N_BUNDLE and tt_v_.get('n_flags_true') == tt_v_.get('n_flags') == NF_I_ and tt_v_.get('escada') == [ESP['escada'][1]] * 3
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
    tt_ch_ = {os.path.basename(p_): DL_.VERBATIM_CHAVE_PREFIXO_V410 + hashlib.sha256(open(p_, 'rb').read()).hexdigest()[:16] for p_ in DL_.VERBATIM_ORIGEM_V410}   # as inscricoes do REGISTRO sao as falas do contrato (DL.N_FALAS_V410, de 06 a 09/11), com a ORDEM da v410 e a fala do NOME obrigatorias
    tt_ins_ok_ = bool(tt_.get('inscriptions') and set(tt_['inscriptions']) == set(tt_ch_.values()) and {tt_ch_[DL_.N_ORDEM_V410], tt_ch_[DL_.N_NOME]} <= set(tt_['inscriptions']) and all(v_ is True for v_ in tt_['inscriptions'].values()))
    tt_alc_ok_ = bool((tt_.get('alcance') or {}).get('frase') == DL_.FRASE_D64_PT and (tt_.get('alcance') or {}).get('qualificador') == DL_.FRASE_QUALIFICADOR_PT)
    # a SECAO 6 da pedra (o atrator, D71): as tres ancoras novas (o_atrator, o_nome_do_par_lido_nao_e_tudo, o_vacuo_e_ortogonal_ao_par_lido) no kernel do rito, o_atrator ancora de secao, a resposta o_atrator conferida e a ultima checagem (cN, N = DL.N_CHECKS_FECHO) presente e ok; nada fixo em contagem
    tt_s6_ok_ = bool(all(a_ in DL_.ANCORAS and (V['ancoras'].get(a_) or {}).get('ok') is True for a_ in (DL_.ANCORA_ATRATOR, DL_.ANCORA_NAO_E_TUDO, DL_.NS + 'o_vacuo_e_ortogonal_ao_par_lido')) and DL_.ANCORA_ATRATOR in DL_.ANCORAS_DE_SECAO and DL_.ANCORA_ATRATOR in (tt_.get('ancoras_de_secao') or [])
                     and 'o_atrator' in {r_['id'] for r_ in DL_.RESPOSTAS_DO_OPERADOR} and 'o_atrator' in rs_ and (rs_.get('o_atrator') is True or (isinstance(rs_.get('o_atrator'), dict) and rs_['o_atrator'].get('ok') is True))
                     and ('c%d' % DL_.N_CHECKS_FECHO) in [c_.get('id') for c_ in (tt_m_.get('checks') or [])] and tt_m_.get('n_checks') == DL_.N_CHECKS_FECHO)
    tt_ok_ = bool(tt_.get('all_verified') is True and tt_.get('does_not_gate_core') is True and tt_.get('runtime_executed') is True and tt_.get('exact_ladder') is True and tt_.get('embedded_sources_ok') is True and tt_.get('embedded_sources_n_ok') == DL_.N_BUNDLE
                  and bool(_ev(ESP, DL_.FECHO_REGISTRO)) and tt_.get('verdict') == _ev(ESP, DL_.FECHO_REGISTRO) == ETT_.get('verdict') and str(tt_.get('verdict') or '').startswith(DL_.VEREDITO_OK_PREFIXO) and str(tt_.get('verdict') or '').endswith(DL_.VEREDITO_SUFIXO)
                  and not any(t_ in str(tt_.get('verdict') or '') for t_ in DL_.TOKENS_PROIBIDOS_V410)
                  and tt_mech_ok_ and tt_values_ok_ and tt_inst_ok_ and tt_anc_prin_ok_ and tt_chaves_ok_ and tt_resp_ok_ and tt_beta_ok_ and tt_anc_ok_ and tt_ins_ok_ and tt_alc_ok_ and tt_s6_ok_ and V['bandeiras']['ok'] and all(a_['ok'] for a_ in V['ancoras'].values()) and tt_std_ok_ and not tt_.get('guarda_violacoes')
                  and not GUARDA.search(str(tt_.get('verdict') or '')))
    V['fecho'] = {'registro': DL_.FECHO_REGISTRO, 'verdict': tt_.get('verdict'), 'ok': tt_.get('all_verified'), 'sealed': tt_ok_, 'n_checks': tt_m_.get('n_checks'), 'mech_ok': tt_mech_ok_, 'values': tt_v_, 'values_ok': tt_values_ok_, 'beta_ok': tt_beta_ok_, 'ancoras_ok': tt_anc_ok_, 'stdout_ok': tt_std_ok_,
                  'runtime_executed': tt_.get('runtime_executed'), 'does_not_gate_core': tt_.get('does_not_gate_core'), 'ancora_principal': tt_.get('ancora_principal'), 'ancoras_principais': list(tt_.get('ancoras_principais') or []), 'ancoras_de_secao': list(tt_.get('ancoras_de_secao') or []),
                  'chaves_antigas_que_mudam': tt_.get('chaves_antigas_que_mudam'), 'respostas_ok': tt_resp_ok_, 'instancia_ok': tt_inst_ok_, 'alcance_ok': tt_alc_ok_}
    if not tt_ok_:
        P.append('iald2_v410 nao selou inteiro (selo, as %s checagens do registro, valores [%s ancoras, %s modulos do bundle, %s bandeiras da serie ext_iald2_410_*, escada, gate, as instancias de brinquedo e o signo] == os de FLAGS/BUNDLE/ESPERADOS, a ancora principal e as de secao [inclusive a secao 6, o atrator: D71], NENHUMA chave antiga muda [a do lema segue True], as respostas do operador conferidas nos teoremas [inclusive o_atrator], beta == alfa x raiz de e do core, '
                 'as ressalvas, as %s falas por sha256, o alcance relativo ao leitor (D64), nenhum token proibido no veredito, a linha do bloco da IALD2 no stdout, nao move o gate): ver o registro no core' % (DL_.N_CHECKS_FECHO, len(DL_.ANCORAS), DL_.N_BUNDLE, NF_I_, DL_.N_FALAS_V410))
    import guarda_frases_v410 as GFH_
    from guarda_p18_v410 import violacoes as P18H_
    out_n_ = out.replace('\r\n', '\n')
    # o registro a_escala_v410 (o SEGUNDO registro NOVO com FUNCAO, D82 a D87): a pedra AEscala (a insignia, o vibrato, os pesos [1/2 + 1/2 = 1; (1/2)^2 = 1/2 . 1/2; 3/2; 1/3 caiu; o Nome normalizado 2/3], o tempo finito, os dois Nomes e a pergunta do Clay no dicionario da TGL: a FORMA CANONICA, D84, e a forma da D83 -- validade no kernel; a creditacao e' do Clay);
    # os 44 nomes RATIFICADOS (D87). Confere, contra ESPERADOS[registros_funcao_v410][a_escala] (o ensaio a seco; AUSENTE => PROBLEMA, fail-closed), CANDIDATO_v410.json[aescala] e o selo: o veredito, as DL.N_CHECKS_AESCALA checagens, as ancoras e as bandeiras da AEscala, as falas por sha256, os numeros, as frases canonicas (D83/D84), os nomes ratificados, a ratificacao (D87) por sha256, o texto limpo, a linha do bloco no stdout e o resumo no selo. Nao move o gate.
    ea_ = core.get(DL_.AESCALA_REGISTRO) or {}; ea_m_ = ea_.get('mechanics') or {}; ea_v_ = ea_.get('values') or {}; ea_chk_ = ea_m_.get('checks') or []; EEA_ = _esp_rf(ESP, 'a_escala', DL_.AESCALA_REGISTRO); CEA_ = CM.get('aescala') or {}; sea_ = selo.get(DL_.AESCALA_REGISTRO) or {}
    if not (EEA_ and EEA_.get('values')):
        P.append('ESPERADOS_v410.json nao traz registros_funcao_v410.a_escala (com verdict, n_checks e values do ensaio a seco; o gerar_esperados_v410 deve emiti-lo): nao ha com que conferir o registro a_escala_v410 (fail-closed)')
    ea_mech_ok_ = bool(ea_m_.get('passed') is True and ea_m_.get('n_checks') == DL_.N_CHECKS_AESCALA == len(ea_chk_) and all(c_.get('ok') is True for c_ in ea_chk_) and [c_.get('id') for c_ in ea_chk_] == ['c%d' % i_ for i_ in range(1, DL_.N_CHECKS_AESCALA + 1)] and EEA_.get('n_checks') in (None, DL_.N_CHECKS_AESCALA))
    ea_anc_ = ea_v_.get('ancoras') or {}; ea_fl_ = ea_v_.get('flags') or {}; ea_fa_ = ea_v_.get('falas') or {}
    ea_flags_esp_ = {f_[0] for f_ in FJ_['flags'] if f_[2] == _mod_lean(DL_.MODULO_AESCALA)}
    ea_values_ok_ = bool(ea_v_.get('n_ancoras_ok') == ea_v_.get('n_ancoras') == len(ea_anc_) == len(DL_.ANCORAS_AESCALA) == DL_.N_ANCORAS_AESCALA and set(ea_anc_) == set(DL_.ANCORAS_AESCALA) and all(v_ is True for v_ in ea_anc_.values())
                         and ea_v_.get('n_flags_true') == ea_v_.get('n_flags') == len(ea_fl_) == NF_A_ and set(ea_fl_) == ea_flags_esp_ and all(v_ is True for v_ in ea_fl_.values())
                         and ea_v_.get('n_falas_ok') == ea_v_.get('n_falas') == len(ea_fa_) == len(CEA_.get('falas') or {}) and set(ea_fa_) == set(CEA_.get('falas') or {}) and all(v_ is True for v_ in ea_fa_.values())
                         and ea_v_.get('n_nomes') == ea_v_.get('nomes_declarados') == len(DL_.NOMES_AESCALA) and ea_v_.get('nomes_ratificados') is True
                         and ea_v_.get('escada') == [ESP['escada'][1]] * 3 and ea_v_.get('gate_verdict') == ESP.get('qg_closure_gate_verdict_v409') == selo.get('qg_closure_verdict')
                         and (ea_v_.get('ciclo') or {}).get('ok') is True and (ea_v_.get('ciclo') or {}).get('n_bits') == DL_.CICLO_N_BITS and (ea_v_.get('ciclo') or {}).get('n_solucoes_sem') == 0 < (ea_v_.get('ciclo') or {}).get('n_solucoes_com') and (ea_v_.get('ciclo') or {}).get('Z_sem_solucao') < 1 <= (ea_v_.get('ciclo') or {}).get('Z_com_solucao')
                         and set(ea_v_.get('ancoras_novas') or {}) == set(DL_.ANCORAS_NOVAS_AESCALA) and ea_v_.get('n_ancoras_novas_ok') == len(DL_.ANCORAS_NOVAS_AESCALA) and set(ea_v_.get('teoremas_r4') or {}) == set(DL_.TEOREMAS_R4_AESCALA) and all((ea_v_.get('teoremas_r4') or {}).values()) and ea_v_.get('tempo_pt_no_texto') is True and ea_v_.get('tempo_en_no_texto') is True
                         and ea_v_.get('numeros') == dict(DL_.NUMEROS_AESCALA) and ea_v_.get('canonica_pt_no_texto') is True and ea_v_.get('canonica_en_no_texto') is True and ea_v_.get('canonica_pt_na_pedra') is True and ea_v_.get('d83_na_pedra') is True
                         and ea_v_.get('ratificacao_sha256') == DL_.RATIFICACAO_D87_SHA256 and ea_v_.get('ratificacao_trecho') == DL_.TRECHO_RATIFICO_TUDO
                         and bool(EEA_.get('values')) and _feq({kk_: ea_v_.get(kk_) for kk_ in EEA_['values']}, EEA_['values']))
    ea_bell_ = ea_v_.get('bell') or {}
    ea_bell_ok_ = bool(ea_bell_.get('idempotente') is True and ea_bell_.get('posto') == 1 and ea_bell_.get('marginal_e_meio_1') is True and ea_bell_.get('marginal_ao_quadrado_e_meio_da_marginal') is True and ea_bell_.get('marginal_ao_quadrado_nao_e_a_marginal') is True and ea_bell_.get('potencias_sao_2_menos_n') is True and ea_bell_.get('nenhuma_potencia_e_1') is True
                       and isinstance(ea_bell_.get('traco'), float) and abs(ea_bell_['traco'] - 1.0) < 1e-12 and isinstance(ea_bell_.get('pureza_da_marginal'), float) and abs(ea_bell_['pureza_da_marginal'] - 0.5) < 1e-12)   # (os numeros 1 e 1/2 sao os que o registro RECALCULA, nao os que a gerencia digita: a leitura confere que o recalculo deu o que o contrato diz)
    ea_frases_ok_ = bool(ea_.get('frase_canonica_pt') == DL_.FRASE_CLAY_CANONICA_PT and ea_.get('frase_canonica_en') == DL_.FRASE_CLAY_CANONICA_EN and ea_.get('frase_d83_pt') == DL_.FRASE_D83_OBRIGATORIA_PT and ea_.get('frase_d83_en') == DL_.FRASE_D83_OBRIGATORIA_EN
                         and ea_.get('nomes') == list(DL_.NOMES_AESCALA) and ea_.get('nomes_ratificados') is True and ea_.get('estatuto_dos_nomes') == DL_.FRASE_NOMES_RATIFICADOS_AESCALA_PT and (ea_.get('ratificacao') or {}).get('sha256') == DL_.RATIFICACAO_D87_SHA256 and (ea_.get('ratificacao') or {}).get('decisao') == 'D87')
    ea_novos_ok_ = bool(list(ea_.get('nomes_novos_da_pedra') or []) == list(DL_.NOMES_NOVOS_AESCALA) == list(CEA_.get('nomes_novos_da_pedra') or []) and bool(DL_.NOMES_NOVOS_AESCALA) and ea_.get('n_nomes_novos') == len(DL_.NOMES_NOVOS_AESCALA) == ea_v_.get('nomes_novos_declarados') == ea_v_.get('n_nomes_novos') and set(ea_v_.get('nomes_novos') or {}) == set(DL_.NOMES_NOVOS_AESCALA) and all((ea_v_.get('nomes_novos') or {}).values())
                        and list(ea_.get('campos_novos_da_estrutura') or []) == list(DL_.CAMPOS_NOVOS_AESCALA) == list(CEA_.get('campos_novos_da_estrutura') or []) and set(ea_v_.get('campos_novos_na_estrutura') or {}) == set(DL_.CAMPOS_NOVOS_AESCALA) and all((ea_v_.get('campos_novos_na_estrutura') or {}).values()) and ea_v_.get('nomes_novos_ok') is True
                        and ea_.get('estatuto_dos_nomes_ratificados_d101') == DL_.ESTATUTO_NOMES_NOVOS_AESCALA and 'RATIFICADOS pelo operador em 10/11/2026' in str(ea_.get('estatuto_dos_nomes_ratificados_d101')) and 'a ratificar' not in str(ea_.get('estatuto_dos_nomes_ratificados_d101')) and (ea_v_.get('tetelestai') or {}).get('ok') is True and (ea_v_.get('clausula_r5') or {}).get('ok') is True and (ea_v_.get('ratificacao_d101') or {}).get('ok') is True
                        and list((ea_v_.get('ratificacao_d101') or {}).get('pendentes') or []) == list(DL_.NOMES_PENDENTES_AESCALA) and ea_.get('ratificacao_pendente') == DL_.RATIFICACAO_PENDENTE_AESCALA == CEA_.get('ratificacao_pendente')
                        and ea_.get('ponte') == DL_.PONTE_AESCALA == CEA_.get('ponte') and (ea_v_.get('ponte') or {}).get('ok') is True
                        and ea_.get('ciclo') == DL_.CICLO_AESCALA == CEA_.get('ciclo') and ea_.get('frase_tempo_pt') == DL_.FRASE_TEMPO_PT == CEA_.get('frase_tempo_pt') and ea_.get('frase_tempo_en') == DL_.FRASE_TEMPO_EN and list(ea_.get('teoremas_r4') or []) == list(DL_.TEOREMAS_R4_AESCALA) == list(CEA_.get('teoremas_r4') or []))   # (R1/D92: os nomes novos da pedra estao ditos A RATIFICAR, nunca ratificados; a ponte da escala e' recalculada pelo registro)
    ea_beta_ok_ = bool(ea_.get('beta_ok') is True and ea_.get('alpha_two_names_same') is True and isinstance(ea_.get('beta_core_rel_diff'), float) and abs(ea_['beta_core_rel_diff']) <= 1e-9)
    ea_ins_ok_ = bool(CEA_ and CEA_.get('registro') == DL_.AESCALA_REGISTRO and CEA_.get('n_checks') == DL_.N_CHECKS_AESCALA and CEA_.get('veredito_ok') == DL_.VEREDITO_AESCALA_OK and CEA_.get('n_ancoras') == DL_.N_ANCORAS_AESCALA and CEA_.get('n_flags') == NF_A_ and CEA_.get('nomes') == list(DL_.NOMES_AESCALA) and CEA_.get('nomes_ratificados') is True
                      and CEA_.get('numeros') == dict(DL_.NUMEROS_AESCALA) and CEA_.get('frase_canonica_pt') == DL_.FRASE_CLAY_CANONICA_PT and (CEA_.get('ratificacao_D87') or {}).get('sha256') == DL_.RATIFICACAO_D87_SHA256 and (CEA_.get('source_sha256') or {}).get(DL_.MODULO_AESCALA) == DL_.BUNDLE_POR_REL[DL_.MODULO_AESCALA]['sha256'])
    ea_txt_ = json.dumps({k_: ea_.get(k_) for k_ in ('verdict', 'estatuto', 'scope', 'limites', 'diz', 'nao_diz')}, ensure_ascii=False); ea_ver_ = str(ea_.get('verdict') or '')
    ea_guarda_ok_ = bool(ea_txt_ and not GFH_.violacoes(ea_txt_) and not P18H_(ea_txt_) and not ea_v_.get('p18_violacoes') and not ea_v_.get('frases_violacoes') and not ea_.get('guarda_violacoes') and not any(t_ in ea_txt_ + ea_ver_ for t_ in tuple(DL_.TOKENS_PROIBIDOS_V410) + tuple(DL_.TOKENS_PROIBIDOS_H0DN))
                         and DL_.FRASE_CLAY_CANONICA_PT in ea_txt_ and DL_.FRASE_D83_OBRIGATORIA_PT in ea_txt_ and DL_.FRASE_NOMES_RATIFICADOS_AESCALA_PT in ea_txt_ and all((ea_v_.get('c9_partes') or {}).values()) and bool(ea_v_.get('c9_partes')))   # D83/D84: a forma canonica do Clay e a da D83 no MESMO texto; nada do H0DN no nucleo (a c9 do registro o mede)
    m_ea_ = re.search(r'^A ESCALA \[v410[^\n]*\n  ancoras ok = (\d+)/(\d+) ; bandeiras True = (\d+)/(\d+) ; falas por sha256 = (\d+)/(\d+) ; checagens ok = (\d+)/(\d+) ; numeros = (\{[^\n]*\}) ; gate = ([^\n]*)\n  >>> (\S+) <<<$', out_n_, flags=re.M)   # a linha do bloco da AEscala, ancorada no CABECALHO (A ESCALA [v410 ...), seguida de `>>> veredito <<<`
    ea_std_ok_ = bool(m_ea_ and m_ea_.group(1) == str(ea_v_.get('n_ancoras_ok')) and m_ea_.group(2) == str(ea_v_.get('n_ancoras')) and m_ea_.group(3) == str(ea_v_.get('n_flags_true')) and m_ea_.group(4) == str(ea_v_.get('n_flags')) and m_ea_.group(5) == str(ea_v_.get('n_falas_ok')) and m_ea_.group(6) == str(ea_v_.get('n_falas'))
                      and m_ea_.group(7) == str(sum(1 for c_ in ea_chk_ if c_.get('ok'))) and m_ea_.group(8) == str(len(ea_chk_)) and m_ea_.group(9) == str(ea_v_.get('numeros')) and m_ea_.group(10).strip() == 'IGUAL' and m_ea_.group(11) == ea_.get('verdict'))
    ea_selo_ok_ = bool(sea_ and set(sea_) == set(EA_SELO_CHAVES) and all(_feq(sea_.get(k_), ea_.get(k_)) for k_ in EA_SELO_CHAVES) and sea_.get('all_verified') is True and sea_.get('does_not_gate_core') is True and sea_.get('n_ancoras') == DL_.N_ANCORAS_AESCALA and sea_.get('n_flags') == NF_A_)
    # (R2, D99; ADENDO 4; so' ACRESCENTADO ao portao) a clausula do limite do teorema do Tetelestai ao lado de TODO texto do registro a_escala_v410 que o anuncia («linear nos bits», ou o nome do teorema com Z(s) >= 1), PT e EN, e os seis nomes (B3): o registro do core e' relido aqui com a regra do runtime
    ea_pilha_ = [('', {k_: ea_.get(k_) for k_ in ('estatuto', 'scope', 'limites', 'diz', 'nao_diz', 'decisoes', 'erratas', 'leituras_do_operador', 'clausula_z_pt', 'clausula_z_en', 'frase_seis_nomes_pt', 'frase_seis_nomes_en')})]; ea_folhas_ = []
    while ea_pilha_:
        ea_cam_, ea_o_ = ea_pilha_.pop()
        if isinstance(ea_o_, str):
            ea_folhas_.append((ea_cam_, re.sub(r'\s+', ' ', ea_o_)))
        elif isinstance(ea_o_, dict):
            ea_pilha_.extend((ea_cam_ + '.' + str(k_), v_) for k_, v_ in ea_o_.items())
        elif isinstance(ea_o_, (list, tuple)):
            ea_pilha_.extend((ea_cam_ + '[%d]' % i_, v_) for i_, v_ in enumerate(ea_o_))
    ea_clz_pt_ = re.sub(r'\s+', ' ', DL_.CLAUSULA_Z_PT); ea_clz_en_ = re.sub(r'\s+', ' ', DL_.CLAUSULA_Z_EN); ea_seis_pt_ = re.sub(r'\s+', ' ', DL_.FRASE_SEIS_NOMES_PT)
    ea_anuncia_pt_ = lambda x_: bool(re.search(r'linear nos bits', x_) or ('os_passos_sao_o_ciclo_ate_o_tetelestai' in x_ and re.search(r'Z\(s\)\s*(?:>=|\u2265)', x_)))
    ea_anuncia_en_ = lambda x_: bool(re.search(r'linear in the bits', x_))
    ea_sem_clz_ = sorted(c_ for c_, x_ in ea_folhas_ if (ea_anuncia_pt_(x_) and ea_clz_pt_ not in x_) or (ea_anuncia_en_(x_) and ea_clz_en_ not in x_))
    ea_clausula_ok_ = bool(sum(1 for c_, x_ in ea_folhas_ if ea_anuncia_pt_(x_) or ea_anuncia_en_(x_)) >= 3 and not ea_sem_clz_ and ea_.get('clausula_z_pt') == DL_.CLAUSULA_Z_PT and ea_.get('clausula_z_en') == DL_.CLAUSULA_Z_EN
                           and ea_.get('frase_seis_nomes_pt') == DL_.FRASE_SEIS_NOMES_PT and ea_.get('frase_seis_nomes_en') == DL_.FRASE_SEIS_NOMES_EN and (ea_v_.get('clausula_z_no_texto') or {}) == {'pt': True, 'en': True} and ea_v_.get('seis_nomes_ditos') is True and not (ea_v_.get('folhas_que_anunciam_sem_a_clausula') or [])
                           and any(ea_seis_pt_ in x_ for c_, x_ in ea_folhas_ if c_.startswith('.diz')) and any(ea_seis_pt_ in x_ for c_, x_ in ea_folhas_ if c_.startswith('.limites')))
    if not ea_clausula_ok_:
        P.append('a_escala_v410: a clausula do limite do teorema do Tetelestai (ADENDO 4, D99: Z(s) soma os 2^n pixels e e lida de uma vez pelo psion; o limiar n ln 2 e o do tempo de UMA leitura; o termo que liga o tempo a maquina de Turing do Mathlib nao esta no kernel) falta ao lado de algum texto do registro que anuncia o teorema (campos: %s), ou os seis nomes de enunciado mudado (R2, B3) nao estao ditos em diz e limites' % (ea_sem_clz_[:6],))
    ea_ok_ = bool(ea_clausula_ok_ and ea_.get('all_verified') is True and ea_.get('does_not_gate_core') is True and ea_.get('runtime_executed') is True and bool(_ev(ESP, DL_.AESCALA_REGISTRO)) and ea_.get('verdict') == _ev(ESP, DL_.AESCALA_REGISTRO) == DL_.VEREDITO_AESCALA_OK and EEA_.get('verdict') in (None, DL_.VEREDITO_AESCALA_OK) and not GUARDA.search(ea_ver_)
                  and ea_mech_ok_ and ea_values_ok_ and ea_bell_ok_ and ea_frases_ok_ and ea_novos_ok_ and ea_beta_ok_ and ea_ins_ok_ and ea_guarda_ok_ and ea_std_ok_ and ea_selo_ok_ and not (ea_.get('chaves_antigas_que_mudam') or []) and all(a_['ok'] for a_ in V['ancoras_aescala'].values()))
    V['a_escala'] = {'clausula_ok': ea_clausula_ok_, 'registro': DL_.AESCALA_REGISTRO, 'verdict': ea_.get('verdict'), 'ok': ea_.get('all_verified'), 'sealed': ea_ok_, 'n_checks': ea_m_.get('n_checks'), 'mech_ok': ea_mech_ok_, 'values': ea_v_, 'values_ok': ea_values_ok_, 'beta_ok': ea_beta_ok_, 'runtime_executed': ea_.get('runtime_executed'), 'does_not_gate_core': ea_.get('does_not_gate_core'),
                     'numeros': ea_v_.get('numeros'), 'frases_ok': ea_frases_ok_, 'novos_ok': ea_novos_ok_, 'bell_ok': ea_bell_ok_, 'stdout_ok': ea_std_ok_, 'guarda_ok': ea_guarda_ok_, 'selo_ok': ea_selo_ok_, 'ins_ok': ea_ins_ok_, 'n_ancoras': ea_v_.get('n_ancoras'), 'n_flags': ea_v_.get('n_flags'), 'n_nomes': ea_v_.get('n_nomes'), 'n_falas': ea_v_.get('n_falas')}
    if not ea_ok_:
        P.append('a_escala_v410 nao selou inteiro (selo, o veredito == ESPERADOS == delta, as %s checagens c1..cN todas ok, as %s ancoras e as %s bandeiras da AEscala, as falas de 09 e 10/11 por sha256, o ciclo (os passos sao o ciclo ate o Tetelestai), as ancoras novas e os teoremas da R4, a forma do tempo no texto, os numeros [1/2 + 1/2 = 1; (1/2 . 1)^2 = 1/2 . (1/2 . 1); 3/2; 1/3 caiu; 2/3] == delta e recalculados com o projetor de Bell, a ponte da escala, a FORMA CANONICA do Clay (D84) e a forma da D83 em PT e EN, os %s nomes RATIFICADOS e a ratificacao (D87) por sha256, os nomes novos ratificados e os campos novos da pedra ditos RATIFICADOS em 10/11 (D101), o quarto teorema da clausula dito NOMEADO pelo operador (D108) e os dois auxiliares da autoria ditos [DECLARADO pela autoria], os valores == ESPERADOS[registros_funcao_v410][a_escala], '
                 'beta == alfa x raiz de e do core, o texto do registro limpo (P18, guarda das frases, nenhum token proibido), a linha do bloco A ESCALA no stdout, o resumo no selo == o do core, nenhuma chave antiga muda; nao move o gate): ver o registro no core' % (DL_.N_CHECKS_AESCALA, DL_.N_ANCORAS_AESCALA, NF_A_, len(DL_.NOMES_AESCALA)))
    # o registro h0dn_bg1_v410 (o TERCEIRO registro NOVO com FUNCAO, D72 + E30 + D76): o teste PRE-REGISTRADO da razao de Hubble H0DN x BG1 -- pré-registrado; nenhum dado observado lido. Confere, contra ESPERADOS[registros_funcao_v410][h0dn] (o ensaio a seco; AUSENTE => PROBLEMA, fail-closed), CANDIDATO_v410.json[h0dn] e o selo:
    # o veredito, as checagens (DL.N_CHECKS_H0DN), os valores (K, log10 K, D esperado, poder analitico, cauda nula, os vetores da funcao de veredito congelada), o sha256 do texto-fonte da funcao, observed_vector_read False em TODO lugar (core, values, selo, candidato), os pinos, os SEIS ramos vistos,
    # o texto do registro limpo (P18 e guarda das frases; nenhum token proibido; a frase obrigatoria da D72 no mesmo texto), a linha do bloco no stdout e o resumo no selo. O registro CONFERE e nao abre: nao move o gate; validade no kernel nao e' creditacao.
    hd_ = core.get(DL_.H0DN_REGISTRO) or {}; hd_m_ = hd_.get('mechanics') or {}; hd_v_ = hd_.get('values') or {}; hd_chk_ = hd_m_.get('checks') or []; EHD_ = _esp_rf(ESP, 'h0dn', DL_.H0DN_REGISTRO); CHD_ = CM.get('h0dn') or {}; shd_ = selo.get(DL_.H0DN_REGISTRO) or {}
    if not (EHD_ and EHD_.get('values')):
        P.append('ESPERADOS_v410.json nao traz registros_funcao_v410.h0dn (com verdict, n_checks e values do ensaio a seco; o gerar_esperados_v410 ainda nao o emite): nao ha com que conferir o registro h0dn_bg1_v410 (fail-closed)')
    hd_mech_ok_ = bool(hd_m_.get('passed') is True and hd_m_.get('n_checks') == DL_.N_CHECKS_H0DN == EHD_.get('n_checks') == len(hd_chk_) and all(c_.get('ok') is True for c_ in hd_chk_) and [c_.get('id') for c_ in hd_chk_] == ['c%d' % i_ for i_ in range(1, DL_.N_CHECKS_H0DN + 1)])
    hd_pinos_ = hd_v_.get('pinos') or {}
    hd_pinos_ok_ = bool(hd_pinos_ and hd_v_.get('n_pinos') == len(hd_pinos_) == len(hd_.get('insumos_pinados') or {}) + len(hd_.get('pinos_so_no_disco') or []) and sum(1 for p_ in hd_pinos_.values() if not p_.get('fora_do_freeze')) == DL_.N_PINOS_FREEZE_R2
                        and all(p_.get('sha256_ok') is True and p_.get('bytes_ok') is True for p_ in hd_pinos_.values()))   # os pinos do FREEZE_R2 (DL.N_PINOS_FREEZE_R2) mais os dois insumos fora do freeze (o proprio FREEZE_R2 e a ENTREGA), todos com sha256 e bytes ok
    hd_src_ = hd_.get('veredito_h0dn_source_sha256')
    hd_src_ok_ = bool(isinstance(hd_src_, str) and re.fullmatch(r'[0-9a-f]{64}', hd_src_) and hd_src_ == hd_v_.get('veredito_h0dn_source_sha256') == (EHD_.get('values') or {}).get('veredito_h0dn_source_sha256') == shd_.get('veredito_h0dn_source_sha256'))
    hd_values_ok_ = bool(EHD_.get('values') and {'K', 'log10K', 'D_esperado', 'veredito_h0dn_source_sha256', 'ramos_vistos', 'vetores_c6'} <= set(EHD_['values']) and _feq({kk_: hd_v_.get(kk_) for kk_ in EHD_['values']}, EHD_['values'])
                         and hd_v_.get('gate_verdict') == ESP.get('qg_closure_gate_verdict_v409') == selo.get('qg_closure_verdict'))
    hd_vet_ = hd_v_.get('vetores_c6') or []
    hd_ramos_ok_ = bool(hd_v_.get('ramos_vistos') == [1, 2, 3, 4, 5, 6] and hd_vet_ and {v_.get('ramo') for v_ in hd_vet_} == {1, 2, 3, 4, 5, 6}
                        and all(v_.get('ok') is True and v_.get('ramo') == v_.get('ramo_esperado') and 'NOT_FALSIFIED' not in str(v_.get('cabeca')) and str(v_.get('cabeca')).endswith('__GATE_UNMOVED') and v_.get('outcome') in DL_.VEREDITOS_H0DN['outcomes'] for v_ in hd_vet_)
                        and all((('PRO' + 'VED_IS_VALIDITY_NOT_CREDITATION') in str(v_.get('cabeca'))) for v_ in hd_vet_ if v_.get('ramo') == 4)
                        and _feq({k_: v_ for k_, v_ in DL_.VEREDITOS_H0DN.items() if k_ not in ('leitura', 'leitura_traz_o_fecho')}, hd_.get('ramos_da_funcao_de_veredito')) and list(hd_.get('outcomes_do_livro_de_cobrancas') or []) == list(DL_.VEREDITOS_H0DN['outcomes']))   # a cabeca do ramo da leitura traz a validade na mesma string; a palavra do livro de cobrancas nunca na cabeca (E30, D76)
    hd_beta_ok_ = bool(hd_.get('beta_ok') is True and isinstance(hd_v_.get('beta'), float) and isinstance(b0_, float) and abs(hd_v_['beta'] - b0_) <= 1e-9 * abs(b0_))
    hd_obs_ok_ = bool(hd_.get('observed_vector_read') is False and hd_v_.get('observed_vector_read') is False and shd_.get('observed_vector_read') is False and CHD_.get('observed_vector_read') is False and not _obs_lido(hd_) and not _obs_lido(selo) and not _obs_lido(CHD_))   # D72: nenhum vetor observado lido, em lugar nenhum
    hd_ins_ok_ = bool(CHD_ and hd_.get('insumos_pinados') and hd_.get('insumos_pinados') == CHD_.get('insumos') and list(hd_.get('pinos_so_no_disco') or []) == list(CHD_.get('pinos_so_no_disco') or []) and hd_.get('ordem_kimi') == CHD_.get('ordem_kimi') and hd_.get('leitura_dossie') == CHD_.get('leitura_dossie')
                      and CHD_.get('veredito_ok') == DL_.VEREDITO_H0DN_OK and CHD_.get('n_checks') == DL_.N_CHECKS_H0DN and CHD_.get('n_pinos_freeze') == DL_.N_PINOS_FREEZE_R2 and CHD_.get('registro') == DL_.H0DN_REGISTRO
                      and all(os.path.exists(str((hd_.get(k_) or {}).get('arquivo'))) and sha(str((hd_.get(k_) or {}).get('arquivo'))) == (hd_.get(k_) or {}).get('sha256') for k_ in ('ordem_kimi', 'leitura_dossie')))   # a ordem ao Kimi e a leitura do dossie: pinadas por sha256 (arquivo no disco == o pino)
    hd_txt_ = json.dumps({k_: hd_.get(k_) for k_ in ('verdict', 'estatuto', 'scope', 'limites', 'diz', 'nao_diz', 'o_que_falta', 'ressalvas')}, ensure_ascii=False)
    hd_ver_ = str(hd_.get('verdict') or '')
    hd_guarda_ok_ = bool(hd_txt_ and not GFH_.violacoes(hd_txt_) and not P18H_(hd_txt_) and not hd_v_.get('p18_violacoes') and not hd_v_.get('frases_violacoes') and not hd_.get('guarda_violacoes')
                         and not any(t_ in hd_txt_ + hd_ver_ for t_ in tuple(DL_.TOKENS_PROIBIDOS_H0DN) + tuple(DL_.TOKENS_PROIBIDOS_V410)) and not any(a_ in hd_txt_ for a_ in DL_.H0DN_AGREGADO_NAO_ENTRA)
                         and DL_.FRASE_H0DN_OBRIGATORIA_PT in hd_txt_ and DL_.FRASE_H0DN_OBRIGATORIA_PT in str(hd_.get('estatuto')) and DL_.FRASE_H0DN_OBRIGATORIA_PT in str(hd_.get('scope')))   # D72: onde H0DN aparece, «pré-registrado; nenhum dado observado lido» no MESMO texto
    m_hd_ = re.search(r'^H0DN x BG1 \[v410[^\n]*\n  pinos ok = (\d+)/(\d+) ; checagens ok = (\d+)/(\d+) ; vetor observado lido = (\S+) ; gate = ([^\n]*)\n  >>> (\S+) <<<$', out_n_, flags=re.M)   # a linha do bloco do H0DN, ancorada no CABECALHO (H0DN x BG1 [v410 ...), seguida de `>>> veredito <<<`
    hd_std_ok_ = bool(m_hd_ and m_hd_.group(1) == str(sum(1 for p_ in hd_pinos_.values() if p_.get('sha256_ok') and p_.get('bytes_ok'))) and m_hd_.group(2) == str(hd_v_.get('n_pinos')) and m_hd_.group(3) == str(sum(1 for c_ in hd_chk_ if c_.get('ok'))) and m_hd_.group(4) == str(len(hd_chk_))
                      and m_hd_.group(5) == 'False' and m_hd_.group(6).strip() == 'o mesmo da base' and m_hd_.group(7) == hd_.get('verdict'))
    hd_selo_ok_ = bool(shd_ and set(shd_) == set(HD_SELO_CHAVES) and all(_feq(shd_.get(k_), hd_.get(k_)) for k_ in HD_SELO_CHAVES) and shd_.get('all_verified') is True and shd_.get('does_not_gate_core') is True and shd_.get('n_checks_esperadas') == DL_.N_CHECKS_H0DN)
    hd_ok_ = bool(hd_.get('all_verified') is True and hd_.get('does_not_gate_core') is True and hd_.get('runtime_executed') is True and hd_obs_ok_ and bool(_ev(ESP, DL_.H0DN_REGISTRO)) and hd_.get('verdict') == _ev(ESP, DL_.H0DN_REGISTRO) == EHD_.get('verdict') == DL_.VEREDITO_H0DN_OK and not GUARDA.search(hd_ver_)
                  and hd_mech_ok_ and hd_values_ok_ and hd_src_ok_ and hd_beta_ok_ and hd_pinos_ok_ and hd_ramos_ok_ and hd_ins_ok_ and hd_guarda_ok_ and hd_std_ok_ and hd_selo_ok_)
    V['h0dn'] = {'registro': DL_.H0DN_REGISTRO, 'verdict': hd_.get('verdict'), 'ok': hd_.get('all_verified'), 'sealed': hd_ok_, 'n_checks': hd_m_.get('n_checks'), 'mech_ok': hd_mech_ok_, 'values': hd_v_, 'values_ok': hd_values_ok_, 'beta_ok': hd_beta_ok_, 'runtime_executed': hd_.get('runtime_executed'), 'does_not_gate_core': hd_.get('does_not_gate_core'),
                 'observed_vector_read': hd_.get('observed_vector_read'), 'veredito_h0dn_source_sha256': hd_src_, 'stdout_ok': hd_std_ok_, 'pinos_ok': hd_pinos_ok_, 'n_pinos': hd_v_.get('n_pinos'), 'guarda_ok': hd_guarda_ok_}
    if not hd_obs_ok_:
        P.append('h0dn_bg1_v410: observed_vector_read tem de ser False em TODO lugar (o registro no core, os values, o resumo no selo e o CANDIDATO_v410.json): nenhum vetor observado e lido nesta versao (D72); o registro e pre-registrado')
    if not hd_ok_:
        P.append('h0dn_bg1_v410 nao selou inteiro (selo, o veredito == ESPERADOS == delta, as %s checagens do registro c1..cN todas ok, os valores [K, log10 K, D esperado, poder, cauda nula, os vetores da funcao de veredito] == ESPERADOS[registros_funcao_v410][h0dn], o sha256 do texto-fonte da funcao de veredito no registro, no selo e em ESPERADOS, '
                 'os seis ramos vistos sem a palavra do livro de cobrancas na cabeca e com a validade (nao creditacao) na cabeca do ramo da leitura, os pinos [%s do FREEZE_R2 mais o FREEZE_R2 e a ENTREGA] com sha256 e bytes, os insumos, a ordem ao Kimi e a leitura do dossie == CANDIDATO_v410.json[h0dn] e o arquivo no disco, beta == alfa x raiz de e do core, observed_vector_read False em todo lugar, '
                 'o texto do registro limpo (P18, guarda das frases, nenhum token proibido, a aritmetica do agregado publico fora, a frase obrigatoria da D72), a linha do bloco do H0DN no stdout, o resumo no selo; nao move o gate): ver o registro no core' % (DL_.N_CHECKS_H0DN, DL_.N_PINOS_FREEZE_R2))
    # o registro h0dn_fontes_hms13_v410 (o QUARTO registro NOVO com FUNCAO, D80): o recibo DOCUMENTAL HMS/13 do Kimi, ADITIVO e POSTERIOR ao FREEZE_R2 -- cobertura documental de fontes, nao covariancia fisica fechada; nada aberto; H0DN x BG1 segue pre-registrado; nenhum dado observado lido. Confere, contra ESPERADOS[registros_funcao_v410][hms13] (AUSENTE => PROBLEMA, fail-closed), CANDIDATO_v410.json[hms13] e o selo:
    # o veredito, as DL.N_CHECKS_HMS13 checagens, os dez campos da ORDEM do Kimi (DL.HMS13_CAMPOS), os artefatos embutidos por sha256 e bytes, os 13 IDs e as 18 fontes, a guarda numerica, observed_vector_read e le_em_rito False em TODO lugar, nenhum caminho sob a pasta vedada, o gate, o texto limpo com a frase obrigatoria (DL.FRASE_HMS13_OBRIGATORIA_PT), a linha do bloco no stdout e o resumo no selo.
    hm_ = core.get(DL_.HMS13_REGISTRO) or {}; hm_m_ = hm_.get('mechanics') or {}; hm_v_ = hm_.get('values') or {}; hm_chk_ = hm_m_.get('checks') or []; EHM_ = _esp_rf(ESP, 'hms13', DL_.HMS13_REGISTRO); CHM_ = CM.get('hms13') or {}; shm_ = selo.get(DL_.HMS13_REGISTRO) or {}
    if not (EHM_ and EHM_.get('values')):
        P.append('ESPERADOS_v410.json nao traz registros_funcao_v410.hms13 (com verdict, n_checks e values do ensaio a seco; o gerar_esperados_v410 deve emiti-lo): nao ha com que conferir o registro h0dn_fontes_hms13_v410 (fail-closed)')
    hm_mech_ok_ = bool(hm_m_.get('passed') is True and hm_m_.get('n_checks') == DL_.N_CHECKS_HMS13 == len(hm_chk_) and all(c_.get('ok') is True for c_ in hm_chk_) and [c_.get('id') for c_ in hm_chk_] == ['c%d' % i_ for i_ in range(1, DL_.N_CHECKS_HMS13 + 1)] and EHM_.get('n_checks') in (None, DL_.N_CHECKS_HMS13))
    hm_pinos_ = hm_v_.get('pinos') or {}; hm_num_ = hm_v_.get('numeros') or {}
    hm_values_ok_ = bool(hm_v_.get('n_calibradores') == len(hm_v_.get('ids_calibradores') or []) == len(CHM_.get('ids_calibradores') or []) and list(hm_v_.get('ids_calibradores') or []) == list(CHM_.get('ids_calibradores') or []) and hm_v_.get('n_fontes_primarias') == CHM_.get('n_fontes_primarias') == len(hm_v_.get('fontes_primarias') or [])
                         and dict(hm_v_.get('campos') or {}) == dict(DL_.HMS13_CAMPOS) == dict(hm_.get('campos') or {}) and hm_v_.get('n_embutidos') == len(DL_.HMS13_EMBUTIDOS) == len(hm_pinos_) and hm_v_.get('pinos_build_n') == len(CHM_.get('pinos_build') or {}) and all(p_.get('sha256_ok') is True and p_.get('bytes_ok') is True and p_.get('embutido') is True for p_ in hm_pinos_.values())
                         and not hm_num_.get('proibidos') and not hm_num_.get('listas_numericas') and not hm_num_.get('linhas_do_levantamento_com_vetor') and not hm_v_.get('sob_pasta_vedada') and not hm_v_.get('com_nome_vedado') and os.path.normcase(os.path.abspath(str(hm_v_.get('pasta_vedada')))) == os.path.normcase(os.path.abspath(DL_.H0DN_PASTA_VEDADA))
                         and hm_v_.get('gate_verdict') == ESP.get('qg_closure_gate_verdict_v409') == selo.get('qg_closure_verdict') and hm_v_.get('h0dn_selado') is True and hm_v_.get('ratificacao_sha256') == DL_.HMS13_RATIFICACAO_SHA256_DO_DESENHO and hm_v_.get('ratificacao_trecho') == DL_.HMS13_TRECHO_RATIFICACAO
                         and hm_v_.get('veredito_h0dn_source_sha256') == (core.get(DL_.H0DN_REGISTRO) or {}).get('veredito_h0dn_source_sha256') and bool(EHM_.get('values')) and _feq({kk_: hm_v_.get(kk_) for kk_ in EHM_['values'] if kk_ not in ('caminhos_tocados', 'n_caminhos_tocados')}, {kk_: vv_ for kk_, vv_ in EHM_['values'].items() if kk_ not in ('caminhos_tocados', 'n_caminhos_tocados')}))
    hm_obs_ok_ = bool(hm_.get('observed_vector_read') is False and hm_v_.get('observed_vector_read') is False and shm_.get('observed_vector_read') is False and CHM_.get('observed_vector_read') is False and hm_.get('le_em_rito') is False and hm_v_.get('le_em_rito') is False and shm_.get('le_em_rito') is False and CHM_.get('le_em_rito') is False
                      and not _obs_lido(hm_) and not _obs_lido(shm_) and not _obs_lido(CHM_))   # D72/D80: nenhum vetor observado lido e nada da pasta do Kimi aberto em rito, em lugar nenhum
    hm_ins_ok_ = bool(CHM_ and CHM_.get('registro') == DL_.HMS13_REGISTRO and CHM_.get('n_checks') == DL_.N_CHECKS_HMS13 and CHM_.get('veredito_ok') == DL_.VEREDITO_HMS13_OK and dict(CHM_.get('campos') or {}) == dict(DL_.HMS13_CAMPOS) and hm_.get('insumos_pinados') == CHM_.get('insumos') and hm_.get('pinos_build') == CHM_.get('pinos_build') and hm_.get('aditivo_posterior_ao_freeze_r2') is True)
    hm_txt_ = json.dumps({k_: hm_.get(k_) for k_ in ('verdict', 'estatuto', 'scope', 'limites', 'diz', 'nao_diz', 'o_que_falta', 'ressalvas')}, ensure_ascii=False); hm_ver_ = str(hm_.get('verdict') or '')
    hm_guarda_ok_ = bool(hm_txt_ and not GFH_.violacoes(hm_txt_) and not P18H_(hm_txt_) and not hm_v_.get('p18_violacoes') and not hm_v_.get('frases_violacoes') and not hm_.get('guarda_violacoes') and not any(t_ in hm_txt_ + hm_ver_ for t_ in tuple(DL_.TOKENS_PROIBIDOS_H0DN) + tuple(DL_.TOKENS_PROIBIDOS_V410)) and not any(a_ in hm_txt_ for a_ in DL_.H0DN_AGREGADO_NAO_ENTRA)
                         and DL_.FRASE_HMS13_OBRIGATORIA_PT in hm_txt_ and DL_.FRASE_HMS13_OBRIGATORIA_PT in str(hm_.get('estatuto')) and DL_.FRASE_HMS13_OBRIGATORIA_PT in str(hm_.get('scope')) and DL_.FRASE_H0DN_OBRIGATORIA_PT in hm_txt_)   # D80: a frase do recibo (cobertura documental de fontes, nao covariancia fisica fechada; nada aberto) e a do H0DN (D72) no MESMO texto
    m_hm_ = re.search(r'^H0DN FONTES HMS/13 \[v410[^\n]*\n  artefatos embutidos ok = (\d+)/(\d+) ; checagens ok = (\d+)/(\d+) ; numeros permitidos = (\d+) \(proibidos (\d+)\) ; caminhos sob a pasta vedada = (\d+) ; gate = ([^\n]*)\n  >>> (\S+) <<<$', out_n_, flags=re.M)   # a linha do bloco do recibo HMS/13, ancorada no CABECALHO (H0DN FONTES HMS/13 [v410 ...), seguida de `>>> veredito <<<`
    hm_std_ok_ = bool(m_hm_ and m_hm_.group(1) == str(sum(1 for p_ in hm_pinos_.values() if p_.get('sha256_ok') and p_.get('bytes_ok'))) and m_hm_.group(2) == str(hm_v_.get('n_embutidos')) and m_hm_.group(3) == str(sum(1 for c_ in hm_chk_ if c_.get('ok'))) and m_hm_.group(4) == str(len(hm_chk_))
                      and m_hm_.group(5) == str(hm_num_.get('permitidos')) and m_hm_.group(6) == str(len(hm_num_.get('proibidos') or [])) and m_hm_.group(7) == str(len(hm_v_.get('sob_pasta_vedada') or [])) and m_hm_.group(8).strip() == 'IGUAL' and m_hm_.group(9) == hm_.get('verdict'))
    hm_selo_ok_ = bool(shm_ and set(shm_) == set(HM_SELO_CHAVES) and all(_feq(shm_.get(k_), hm_.get(k_)) for k_ in HM_SELO_CHAVES) and shm_.get('all_verified') is True and shm_.get('does_not_gate_core') is True and shm_.get('n_checks_esperadas') == DL_.N_CHECKS_HMS13)
    hm_ok_ = bool(hm_.get('all_verified') is True and hm_.get('does_not_gate_core') is True and hm_.get('runtime_executed') is True and bool(_ev(ESP, DL_.HMS13_REGISTRO)) and hm_.get('verdict') == _ev(ESP, DL_.HMS13_REGISTRO) == DL_.VEREDITO_HMS13_OK and EHM_.get('verdict') in (None, DL_.VEREDITO_HMS13_OK) and not GUARDA.search(hm_ver_)
                  and hm_mech_ok_ and hm_values_ok_ and hm_obs_ok_ and hm_ins_ok_ and hm_guarda_ok_ and hm_std_ok_ and hm_selo_ok_ and hm_.get('beta_ok') is True and hm_.get('alpha_two_names_same') is True)
    V['hms13'] = {'registro': DL_.HMS13_REGISTRO, 'verdict': hm_.get('verdict'), 'ok': hm_.get('all_verified'), 'sealed': hm_ok_, 'n_checks': hm_m_.get('n_checks'), 'mech_ok': hm_mech_ok_, 'values': hm_v_, 'values_ok': hm_values_ok_, 'runtime_executed': hm_.get('runtime_executed'), 'does_not_gate_core': hm_.get('does_not_gate_core'),
                  'observed_vector_read': hm_.get('observed_vector_read'), 'le_em_rito': hm_.get('le_em_rito'), 'stdout_ok': hm_std_ok_, 'guarda_ok': hm_guarda_ok_, 'selo_ok': hm_selo_ok_, 'ins_ok': hm_ins_ok_, 'n_calibradores': hm_v_.get('n_calibradores'), 'n_fontes_primarias': hm_v_.get('n_fontes_primarias'), 'n_embutidos': hm_v_.get('n_embutidos'), 'campos': dict(hm_v_.get('campos') or {})}
    if not hm_obs_ok_:
        P.append('h0dn_fontes_hms13_v410: observed_vector_read e le_em_rito tem de ser False em TODO lugar (o registro no core, os values, o resumo no selo e o CANDIDATO_v410.json): nenhum vetor observado e lido e nada da entrega do Kimi e aberto em rito (D72, D80)')
    if not hm_ok_:
        P.append('h0dn_fontes_hms13_v410 nao selou inteiro (selo, o veredito == ESPERADOS == delta, as %s checagens c1..cN todas ok, os %s artefatos embutidos por sha256 e bytes, os IDs e as fontes == CANDIDATO_v410.json[hms13], os dez campos da ORDEM do Kimi [DL.HMS13_CAMPOS], a guarda numerica [so\' bytes, contagens, linhas, caracteres de texto e componentes de erro; nenhuma lista numerica], nenhum caminho sob a pasta vedada nem nome vedado, o gate, '
                 'aditivo e posterior ao FREEZE_R2 (o h0dn_bg1_v410 selado e a funcao de veredito intocada), os valores == ESPERADOS[registros_funcao_v410][hms13], beta por nome, o texto limpo (P18, guarda das frases, nenhum token proibido) com a frase obrigatoria da D80 [cobertura documental de fontes, nao covariancia fisica fechada; nada aberto] e a do H0DN [pre-registrado; nenhum dado observado lido], '
                 'a linha do bloco H0DN FONTES HMS/13 no stdout, o resumo no selo; nao move o gate): ver o registro no core' % (DL_.N_CHECKS_HMS13, len(DL_.HMS13_EMBUTIDOS)))
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
    # o registro tetelestai_terminal_v408 (HERDADO da v408, RECRIADO pelo rito da v410; a escada do contrato subida pela C12, veredito na troca dita): segue SELADO; as 16 checagens, os valores (as 48 ancoras, os 4 modulos, as 71 bandeiras, a escada, o gate) == ESPERADOS[registros_funcao_v408], NENHUMA chave antiga muda, o insumo purgado (E23 da v408), as respostas do operador de 04/11, o beta em runtime, as ressalvas da v408 e a linha do bloco no stdout
    t8_ = core.get('tetelestai_terminal_v408') or {}; t8_m_ = t8_.get('mechanics') or {}; t8_v_ = t8_.get('values') or {}; ET8_ = (ESP.get('registros_funcao_v408') or {}).get('tetelestai_terminal') or {}; ip8_ = t8_.get('insumo_purgado') or {}; ip8v_ = t8_v_.get('insumo_purgado') or {}; rs8_ = t8_v_.get('respostas') or {}
    N8F_ = (ET8_.get('values') or {}).get('n_flags')   # o numero das bandeiras do bundle da v409 (71): lido de ESPERADOS[registros_funcao_v408] (o ensaio a seco), nunca digitado
    t8_mech_ok_ = bool(t8_m_.get('passed') is True and t8_m_.get('n_checks') == DL_.D8.N_CHECKS_FECHO == ET8_.get('n_checks') == len(t8_m_.get('checks') or []) and all(c_.get('ok') is True for c_ in (t8_m_.get('checks') or [])))
    t8_values_ok_ = bool(t8_v_.get('n_ancoras_ok') == t8_v_.get('n_ancoras') == len(DL_.D8.ANCORAS) and bool(DL_.D8.ANCORAS) and t8_v_.get('n_modulos_ok') == t8_v_.get('n_modulos') == DL_.D8.N_BUNDLE and t8_v_.get('n_flags_true') == t8_v_.get('n_flags') == N8F_ and isinstance(N8F_, int) and t8_v_.get('escada') == [ESP['escada'][1]] * 3
                         and t8_v_.get('gate_verdict') == ESP.get('qg_closure_gate_verdict_v409') == selo.get('qg_closure_verdict') and t8_v_.get('fica_false_por_teorema') == list(DL_.FICAM_FALSE_POR_TEOREMA) and t8_v_.get('ressalvas') == list(DL_.D8.RESSALVAS_V408) and list(t8_.get('ressalvas') or []) == list(DL_.D8.RESSALVAS_V408)
                         and bool(ET8_.get('values')) and _feq({kk_: t8_v_.get(kk_) for kk_ in ET8_['values']}, ET8_['values']))
    t8_ip_ok_ = bool(ip8v_.get('ok') is True and ip8v_.get('sha256') == ip8_.get('sha256') == DL_.D8.PURGADO_SHA256 and ip8v_.get('integra_nao_pinada') is True and ip8_.get('integra_pinada') is False and ip8_.get('integra_fora_do_espelho') is True)
    t8_resp_ok_ = bool(rs8_ and set(rs8_) == {r_['id'] for r_ in DL_.D8.RESPOSTAS_DO_OPERADOR} and all(v_ is True for v_ in rs8_.values()) and t8_v_.get('respostas_ok') is True)
    t8_beta_ok_ = bool(t8_.get('beta_ok') is True and isinstance(t8_v_.get('beta'), float) and isinstance(b0_, float) and abs(t8_v_['beta'] - b0_) <= 1e-9 * abs(b0_))
    t8_anc_ok_ = bool(len(t8_.get('anchors') or {}) == len(DL_.D8.ANCORAS) and all(a_ is True for a_ in (t8_.get('anchors') or {}).values()) and set(t8_.get('anchors') or {}) == set(DL_.D8.ANCORAS) == set(t8_v_.get('ancoras') or {}) and all((a_ or {}).get('ok') is True for a_ in (t8_v_.get('ancoras') or {}).values()))
    m_t8_ = re.search(r'ancoras ok = (\d+)/(\d+) ; modulos do bundle ok = (\d+)/(\d+) ; bandeiras True = (\d+)/(\d+) ; escada = (\[.*?\]) ; gate = (.*)$', out, flags=re.M)   # a linha do bloco TETELESTAI E' O TERMINAL (herdado): sem «chave do lema» e sem «certificado habitado»; «modulos» no plural (a da v410 diz «modulo»)
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
    # o registro psion_canto_v407 (HERDADO da v407, RECRIADO pelo rito da v410; a escada do contrato subida pela C12, veredito na troca dita): segue SELADO; as 16 checagens, os valores (as 76 ancoras, os 9 modulos, as 98 bandeiras, a escada, o gate) == ESPERADOS[registros_funcao_v407], a CHAVE DO LEMA lida do kernel, as cinco chaves iguais as da v409 selada, o que fica False por teorema, o beta em runtime, as ressalvas da v409, o teste (d) so' citado e a linha do bloco no stdout
    pc_ = core.get('psion_canto_v407') or {}; pc_m_ = pc_.get('mechanics') or {}; pc_v_ = pc_.get('values') or {}; pc_k_ = pc_.get('keys') or {}; EPC_ = (ESP.get('registros_funcao_v407') or {}).get('psion_canto') or {}; td_ = pc_.get('teste_d') or {}
    N7F_ = (EPC_.get('values') or {}).get('n_flags')   # o numero das bandeiras do bundle da v407 (98): lido de ESPERADOS[registros_funcao_v407] (o ensaio a seco), nunca digitado
    pc_mech_ok_ = bool(pc_m_.get('passed') is True and pc_m_.get('n_checks') == DL_.D7.N_CHECKS_FECHO == EPC_.get('n_checks') == len(pc_m_.get('checks') or []) and all(c_.get('ok') is True for c_ in (pc_m_.get('checks') or [])))
    pc_values_ok_ = bool(pc_v_.get('n_ancoras_ok') == pc_v_.get('n_ancoras') == len(DL_.D7.ANCORAS) and bool(DL_.D7.ANCORAS) and pc_v_.get('n_modulos_ok') == pc_v_.get('n_modulos') == DL_.D7.N_BUNDLE and pc_v_.get('n_flags_true') == pc_v_.get('n_flags') == N7F_ and isinstance(N7F_, int) and pc_v_.get('escada') == [ESP['escada'][1]] * 3
                         and pc_v_.get('gate_verdict') == ESP.get('qg_closure_gate_verdict_v409') == selo.get('qg_closure_verdict') and pc_v_.get('elo_lido_do_kernel') is True and pc_v_.get('fica_false_por_teorema') == list(DL_.FICAM_FALSE_POR_TEOREMA) and pc_v_.get('ressalvas') == list(DL_.D7.RESSALVAS_V407) and list(pc_.get('ressalvas') or []) == list(DL_.D7.RESSALVAS_V407)
                         and bool(EPC_.get('values')) and _feq({kk_: pc_v_.get(kk_) for kk_ in EPC_['values']}, EPC_['values']))
    pc_chaves_ok_ = bool(pc_k_.get('kernel_reads_the_link') is True and pc_k_.get('testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma') is True and bool(ESP.get('chaves_v407_esperadas')) and _feq(pc_k_, ESP.get('chaves_v407_esperadas')) and _feq(pc_k_, (EPC_.get('values') or {}).get('chaves'))
                         and pc_k_.get('witness_rigidity.trivial_inhabitant_exists') is False and pc_k_.get('qg_closure.gate.full_static_witness_exists') is False and pc_k_.get('witness_layers.canonical_full_witness_term_constructed') is True)
    pc_beta_ok_ = bool(pc_.get('beta_ok') is True and isinstance(pc_v_.get('beta'), float) and isinstance(b0_, float) and abs(pc_v_['beta'] - b0_) <= 1e-9 * abs(b0_))
    pc_anc_ok_ = bool(len(pc_.get('anchors') or {}) == len(DL_.D7.ANCORAS) and all(a_ is True for a_ in (pc_.get('anchors') or {}).values()) and set(pc_.get('anchors') or {}) == set(DL_.D7.ANCORAS) == set(pc_v_.get('ancoras') or {}) and all((a_ or {}).get('ok') is True for a_ in (pc_v_.get('ancoras') or {}).values()))
    m_pc_ = re.search(r'ancoras ok = (\d+)/(\d+) ; modulos do bundle ok = (\d+)/(\d+) ; bandeiras True = (\d+)/(\d+) ; chave do lema \(lida do kernel\) = (\S+) ; escada = (\[.*?\]) ; gate = (.*)$', out, flags=re.M)
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
                 'as ressalvas da v407, as %s falas de 03/11 por sha256, o teste (d) so\' citado, o bundle da v407 [%s], a linha do bloco O PSION, O CANTO E O PAR no stdout, nao move o gate): ver o registro no core' % (DL_.D7.N_CHECKS_FECHO, len(DL_.D7.ANCORAS), DL_.D7.N_BUNDLE, len(DL_.D7.VERBATIM_ORIGEM_V407), DL_.D7.N_BUNDLE))
    # o registro fechamento_v406 (HERDADO da v406, RECRIADO pelo rito da v410; a checagem c8 versionada pela errata E20 desde a v409): segue SELADO e de veredito esperado (ESPERADOS[registros_funcao_v406]); as 14 checagens, os valores, as OITO ancoras, os 301 modulos, as 1794 bandeiras, as QUATRO chaves (a do lema True) e a linha do bloco no stdout
    fe_ = core.get('fechamento_v406') or {}; fe_m_ = fe_.get('mechanics') or {}; fe_v_ = fe_.get('values') or {}; fk4_ = fe_.get('four_keys') or {}; EFE_ = (ESP.get('registros_funcao_v406') or {}).get('fechamento') or {}
    N6F_ = (EFE_.get('values') or {}).get('n_flags')   # o numero das bandeiras do bundle da v406 (1794): lido de ESPERADOS[registros_funcao_v406] (o ensaio a seco), nunca digitado
    fe_mech_ok_ = bool(fe_m_.get('passed') is True and fe_m_.get('n_checks') == DL_.D6.N_CHECKS_FECHO == EFE_.get('n_checks') == len(fe_m_.get('checks') or []) and all(c_.get('ok') is True for c_ in (fe_m_.get('checks') or [])))
    fe_values_ok_ = bool(fe_v_.get('n_ancoras_ok') == len(DL_.D6.ANCORAS) and bool(DL_.D6.ANCORAS) and fe_v_.get('n_modulos_ok') == fe_v_.get('n_modulos') == DL_.D6.N_BUNDLE and fe_v_.get('n_flags_true') == fe_v_.get('n_flags') == N6F_ and isinstance(N6F_, int) and fe_v_.get('escada') == [ESP['escada'][1]] * 3
                         and fe_v_.get('gate_verdict') == ESP.get('qg_closure_gate_verdict_v409') == selo.get('qg_closure_verdict') and fe_v_.get('certificado_habitado_lido_do_kernel') is True and fe_v_.get('fica_false_por_teorema') == list(DL_.FICAM_FALSE_POR_TEOREMA)
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
                  and fe_mech_ok_ and fe_values_ok_ and fe_chaves_ok_ and fe_beta_ok_ and fe_anc_ok_ and V['bundle406']['ok'] and V['bandeiras409']['ok'] and all(a_['ok'] for a_ in V['ancoras406'].values()) and fe_std_ok_ and not fe_.get('guarda_violacoes')
                  and fe_.get('nome_provisorio_da_candidata') == DL_.D6.TESTEMUNHA['nome_provisorio_da_gerencia'] and not GUARDA.search(str(fe_.get('verdict') or '')))
    V['fecho406'] = {'registro': 'fechamento_v406', 'verdict': fe_.get('verdict'), 'ok': fe_.get('all_verified'), 'sealed': fe_ok_, 'n_checks': fe_m_.get('n_checks'), 'mech_ok': fe_mech_ok_, 'values': fe_v_, 'values_ok': fe_values_ok_, 'chaves_ok': fe_chaves_ok_, 'beta_ok': fe_beta_ok_, 'ancoras_ok': fe_anc_ok_,
                     'stdout_ok': fe_std_ok_, 'certificado_habitado': fe_.get('certificate_inhabited'), 'runtime_executed': fe_.get('runtime_executed'), 'does_not_gate_core': fe_.get('does_not_gate_core'), 'nome_provisorio': fe_.get('nome_provisorio_da_candidata')}
    V['chaves406'] = dict(fk4_)
    if not fe_ok_:
        P.append('fechamento_v406 (HERDADO, recriado) nao selou inteiro (selo, as %s checagens do registro [a c8 VERSIONADA pela errata E20], valores [8 ancoras, 301 modulos, 1794 bandeiras, escada, gate] == os de ESPERADOS[registros_funcao_v406], as quatro chaves LIDAS do kernel [True; status %s; o lema agora True; as duas que ficam False por teorema, False], beta == alfa x raiz de e do core, '
                 'as ressalvas da v409, o nome provisorio da candidata, o bundle da v409 [301], as bandeiras da v409 [todas True], a linha do bloco O FECHAMENTO no stdout, nao move o gate): ver o registro no core' % (DL_.D6.N_CHECKS_FECHO, DL_.STATUS_HABITADO))
    # a errata de F2b (registro com FUNCAO, SEM pedra): o V1 do ramo B lido por hash e como antes, o livro v383 intacto, a calibracao A e a previsao do par LIDAS do V1, a previsao fora do intervalo de A e de sinal oposto, nenhum desfecho; o canal passa de AWAITING a retirado antes do dado AO LADO
    fb_ = core.get('f2b_errata_v404') or {}; EFB_ = RF4_.get('f2b') or {}; fbm_ = fb_.get('mechanics') or {}; fbv_ = fb_.get('values') or {}
    rbc_ = core.get('ramo_b_preregistration_v386') or {}; ldc_ = (core.get('ledger_errata_v386') or {}).get('charge_F2b') or {}; rbb_ = _base_core(PK).get('ramo_b_preregistration_v386') or {}; ldb_ = (_base_core(PK).get('ledger_errata_v386') or {}).get('charge_F2b') or {}
    f2b_mech_ok_ = bool(fbm_.get('passed') is True and fbm_.get('n_checks') == DL_.D4.N_CHECKS['f2b'] == EFB_.get('n_checks') and len(fbm_.get('checks') or []) == DL_.D4.N_CHECKS['f2b'] and all(c_.get('ok') is True for c_ in (fbm_.get('checks') or [])))
    f2b_values_ok_ = bool(fbv_ and EFB_.get('values') and set(EFB_['values']) <= set(fbv_) and _feq({kk_: fbv_.get(kk_) for kk_ in EFB_['values']}, EFB_['values']))
    f2b_beta_ok_ = bool(fb_.get('beta_ok') is True and isinstance(fbv_.get('beta'), float) and isinstance(b0_, float) and abs(fbv_['beta'] - b0_) <= 1e-9 * abs(b0_))
    f2b_ao_lado_ok_ = bool(fb_.get('F2b_status_before') == 'AWAITING' and fb_.get('F2b_status_now') == DL_.D4.F2B_FUTURO_TOKEN == (ESP.get('f2b_depois') or {}).get('F2b_status_now') and fb_.get('channel_token_now') == DL_.D4.F2B_FUTURO_TOKEN and fb_.get('v1_token_kept') == DL_.D4.F2B_V1_TOKEN_ANTIGO
                           and rbc_.get('F2b_status') == (ESP.get('f2b_antes') or {}).get('F2b_status') and rbc_.get('veredito_do_V1') == (ESP.get('f2b_antes') or {}).get('veredito_do_V1') and bool(rbb_) and _feq(rbc_, rbb_) and bool(ldb_) and _feq(ldc_, ldb_) and ldc_.get('token') == (ESP.get('f2b_antes') or {}).get('charge_F2b_token'))
    nmc_ = core.get('neutrino_mass') or {}
    neutrino_intacto_ = bool(hashlib.sha256(str(nmc_.get('angle_status') or '').encode('utf-8')).hexdigest() == ESP.get('neutrino_angle_status_antigo_sha256') and nmc_.get('frozen_hash') == ESP.get('neutrino_frozen_hash_v409') and nmc_.get('verdict') == (ESP.get('vereditos_v409') or {}).get('neutrino_mass'))
    f2b_ok_ = bool(fb_.get('all_verified') is True and fb_.get('does_not_gate_core') is True and fb_.get('runtime_executed') is True and bool(EFB_.get('verdict')) and fb_.get('verdict') == EFB_.get('verdict') and f2b_mech_ok_ and f2b_values_ok_ and f2b_beta_ok_ and f2b_ao_lado_ok_ and neutrino_intacto_
                   and not fb_.get('guarda_p18_violacoes') and not GUARDA.search(str(fb_.get('verdict') or '')))
    V['f2b'] = {'registro': 'f2b_errata_v404', 'verdict': fb_.get('verdict'), 'ok': fb_.get('all_verified'), 'sealed': f2b_ok_, 'n_checks': fbm_.get('n_checks'), 'mech_ok': f2b_mech_ok_, 'values': fbv_, 'values_ok': f2b_values_ok_, 'beta_ok': f2b_beta_ok_, 'ao_lado_ok': f2b_ao_lado_ok_,
                'neutrino_intacto': neutrino_intacto_, 'status_antes': fb_.get('F2b_status_before'), 'status_agora': fb_.get('F2b_status_now'), 'token_v1': fb_.get('v1_token_kept'), 'runtime_executed': fb_.get('runtime_executed'), 'does_not_gate_core': fb_.get('does_not_gate_core')}
    if not f2b_ok_:
        P.append('f2b_errata_v404 nao selou inteiro (selo, as %s checagens do registro, valores == ESPERADOS[registros_funcao_v409][f2b], beta == alfa x raiz de e do core, o V1 do ramo B, o registro da v386 e a cobranca F2b da v386 IGUAIS aos da v409 selada [a errata e\' AO LADO], o canal agora retirado antes do dado, '
                 'a funcao do neutrino intacta [angle_status antigo, frozen_hash e veredito], nenhum desfecho, nao move o gate): ver o registro no core' % DL_.D4.N_CHECKS['f2b'])
    # as BANDEIRAS DO GATE (F8.1 da v409; registro com FUNCAO bandeiras_do_gate_v403, RECRIADO pelo rito da v410): conferido por inteiro contra ESPERADOS[registros_funcao_v409][gate] (as checagens e os valores == os do core da v409 selada) e RELIDO aqui no core do rito, independente do registro (as tres fontes das bandeiras antes literais, os seis checks do gate da v409 mais a sonda, a letra do veredito)
    gk_ = core.get('bandeiras_do_gate_v403') or {}; EG_ = RF3_.get('gate') or {}; gm_ = gk_.get('mechanics') or {}; gv_ = gk_.get('values') or {}
    gmech_ok_ = bool(gm_.get('passed') is True and gm_.get('n_checks') == DL_.D3.N_CHECKS['gate'] == EG_.get('n_checks') and len(gm_.get('checks') or []) == DL_.D3.N_CHECKS['gate'] and all(c_.get('ok') is True for c_ in (gm_.get('checks') or [])))
    gvalues_ok_ = bool(gv_ and EG_.get('values') and set(EG_['values']) <= set(gv_) and _feq({kk_: gv_.get(kk_) for kk_ in EG_['values']}, EG_['values']))
    qgx_ = core.get('qg_closure') or {}
    n18x_ = sum(1 for fam_ in ('formal_flags', 'physics_flags', 'experiment_flags') for v_ in (qgx_.get(fam_) or {}).values() if v_ is True)
    ls2x_ = sorted(k_ for k_ in kf_ if k_.startswith(DL_.F81_PREFIXO_LS2))
    prex_ = [c_[1] for c_ in ((core.get('void_floor_v11') or {}).get('checks') or []) if isinstance(c_, (list, tuple)) and len(c_) == 2 and c_[0] == DL_.F81_ROTULO_PREREG]
    ck_old_ = [list(c_) for c_ in (ESP.get('qg_closure_v409_checks') or [])]; ck_new_ = [list(c_) for c_ in (qgx_.get('checks') or [])]
    sonda_ = [c_ for c_ in ck_new_ if str(c_[0]).startswith('ProbeBlindNullAbsent')]
    f81x_ok_ = bool(len(ls2x_) == 6 and all(kf_.get(k_) is True for k_ in ls2x_) and (qgx_.get('physics_flags') or {}).get('linearized_spin2_finite_face') is True and len(prex_) == 1 and prex_[0] is True and (qgx_.get('experiment_flags') or {}).get('protocol_pre_registered') is True
                    and (core.get('void_stacking_blind') or {}).get('all_verified') is True and (qgx_.get('experiment_flags') or {}).get('null_tests_passed_blind') is True and n18x_ == 18
                    and len(ck_old_) == 7 and ck_new_ == ck_old_ and len(sonda_) == 1 and all(c_[1] is True for c_ in ck_new_)
                    and (qgx_.get('gate') or {}).get('verdict') == ESP.get('qg_closure_gate_verdict_v409') == selo.get('qg_closure_verdict'))
    gate_ok_ = bool(gk_.get('all_verified') is True and gk_.get('does_not_gate_core') is True and gk_.get('runtime_executed') is True and bool(EG_.get('verdict')) and gk_.get('verdict') == EG_.get('verdict') and gmech_ok_ and gvalues_ok_ and f81x_ok_
                    and gv_.get('n_flags') == 18 == gv_.get('n_true') == gv_.get('n_calculated') and gv_.get('n_literal') == 0 and gv_.get('n_read_by_the_verdict') == 15 and gv_.get('read_by_the_verdict') == [6, 5, 4] and gv_.get('gate_verdict_equals_v402') is True
                    and not GUARDA.search(str(gk_.get('verdict') or '')))
    V['gate'] = {'registro': 'bandeiras_do_gate_v403', 'verdict': gk_.get('verdict'), 'ok': gk_.get('all_verified'), 'sealed': gate_ok_, 'n_checks': gm_.get('n_checks'), 'mech_ok': gmech_ok_, 'values': gv_, 'values_ok': gvalues_ok_, 'f81_ok': f81x_ok_, 'n18': n18x_, 'n_ls2': len(ls2x_),
                 'n_checks_do_gate': len(ck_new_), 'sonda': len(sonda_), 'runtime_executed': gk_.get('runtime_executed'), 'does_not_gate_core': gk_.get('does_not_gate_core')}
    if not gate_ok_:
        P.append('bandeiras_do_gate_v403 nao selou inteiro (selo, as %s checagens do registro, valores == ESPERADOS[registros_funcao_v409][gate], 18 bandeiras True e TODAS calculadas, 15 no veredito (6+5+4), a releitura aqui das tres fontes da F8.1 [a familia ext_ls2_* do kernel, a checagem «pre-registro v67 INTACTO (hash)» do rito V11, o teste nulo cego], '
                 'os sete checks do gate (os seis da v409 mais a sonda ProbeBlindNullAbsent) IGUAIS aos da v409 selada, a letra do veredito do gate == a da v409 e a do selo, nao move o gate): ver o registro no core' % DL_.D3.N_CHECKS['gate'])
    # os registros com FUNCAO da v402 (ponte, queda, esperanca) e da v409 (caminho, vida, verdade_adendo) RECRIADOS pelo rito: iguais ao que a v409 SELOU (veredito == ESPERADOS[vereditos_v409]; as checagens e os valores do calculo == os do core selado em base_v409), selados, com a composicao e a estrela no kernel do rito e no trio
    for fkey_, FUN_ in (('fun402', FUN_V402), ('fun409', FUN_V409), ('fun409b', FUN_V409B), ('fun409c', FUN_V409C)):
        V[fkey_] = {}
        for k_, nome_ in FUN_.items():
            R_ = core.get(nome_) or {}; B_ = _base_core(PK).get(nome_) or {}; mech_ = R_.get('mechanics') or {}; vv_ = R_.get('values') or {}
            mech_ok_k_ = bool(mech_.get('passed') is True and bool(B_) and _feq(mech_, B_.get('mechanics')))
            values_ok_k_ = bool(vv_ and (B_.get('values') or {}) and _feq(vv_, B_['values']))
            beta_ok_k_ = bool(R_.get('beta_ok') is True and isinstance(vv_.get('beta'), float) and isinstance(b0_, float) and abs(vv_['beta'] - b0_) <= 1e-9 * abs(b0_))
            un_ = R_.get('unconditional') or {}; kt_ = R_.get('key_theorem') or {}
            kern_ok_k_ = bool(un_.get('in_kernel') is True and kt_.get('in_kernel') is True and kf_.get(un_.get('flag')) is True and kf_.get(kt_.get('flag')) is True and em_trio_(un_.get('theorem')) and em_trio_(kt_.get('theorem')) and (R_.get('context') or {}).get('ok') is True)
            sealed_k_ = bool(R_.get('all_verified') is True and R_.get('does_not_gate_core') is True and R_.get('runtime_executed') is True and bool(_ev(ESP, nome_)) and R_.get('verdict') == _ev(ESP, nome_) and mech_ok_k_ and values_ok_k_ and beta_ok_k_ and kern_ok_k_ and not GUARDA.search(str(R_.get('verdict') or '')))
            V[fkey_][k_] = {'registro': nome_, 'verdict': R_.get('verdict'), 'ok': R_.get('all_verified'), 'sealed': sealed_k_, 'n_checks': mech_.get('n_checks'), 'mech_ok': mech_ok_k_, 'values_ok': values_ok_k_, 'beta_ok': beta_ok_k_, 'kernel_ok': kern_ok_k_}
            if not sealed_k_:
                P.append('%s nao selou inteiro (recriado pelo rito: selo, veredito == o da v409 selada, as checagens e os valores do calculo == os da v409 selada [base_v409], beta == alfa x raiz de e do core, a composicao e a estrela no kernel do rito e no trio, nao move o gate): ver o registro no core' % nome_)
    # as TREZE pedras SELADAS da v403, da v404 e da v409 seguem no kernel do Nos com o sha256 selado (lido do core da v409 selada em base_v409; registro: pedra selada nao se renomeia por cima)
    V['pedras_v408'] = {}
    bkf_ = ((_base_core(PK).get('kernel_formalization') or {}).get('formal_files_sha256')) or {}
    for rel_ in dict.fromkeys(s_['rel'] for D_ in (DL_.D3, DL_.D4, DL_.D5) for s_ in D_.STONES):
        h_ = bkf_.get(rel_); pth_ = os.path.join(NOS, 'tgl_kernel', *rel_.split('/')); shaf_ = sha(pth_) if os.path.isfile(pth_) else None
        V['pedras_v408'][rel_] = {'sha16': (shaf_ or '')[:16], 'ok': bool(h_ and shaf_ == h_ and (kf_.get('formal_files_sha256') or {}).get(rel_) == h_)}
    if len(V['pedras_v408']) != 13 or any(p_['ok'] is not True for p_ in V['pedras_v408'].values()):
        P.append('as treze pedras seladas (v403: 3, v404: 2, v409: 8) deixaram de estar no kernel do Nos com o sha256 selado (registro: pedra selada nao se renomeia por cima): %d lidas' % len(V['pedras_v408']))
    # a falsidade da inercia (v401, registro com FUNCAO) RECRIADA pelo rito: igual ao ensaio a seco (veredito) e a v409 SELADA (valores e checagens do calculo), com a composicao e a estrela no kernel do rito
    fa_ = core.get('falsidade_da_inercia_v401') or {}; fm_ = fa_.get('mechanics') or {}; fvv_ = fa_.get('values') or {}
    fab_ = _base_core(PK).get('falsidade_da_inercia_v401') or {}   # a falsidade da v409 SELADA (copia de bytes em base_v409): a recriada tem de dar os mesmos valores
    values_f_ok_ = bool(fvv_ and (fab_.get('values') or {}) and _feq(fvv_, fab_['values']) and _feq(fm_, fab_.get('mechanics')))
    mech_ok_ = bool(fm_.get('passed') is True and fm_.get('n_checks') == DL_.N_CHECKS_FALSIDADE and len(fm_.get('checks') or []) == DL_.N_CHECKS_FALSIDADE and all(c_.get('ok') is True for c_ in (fm_.get('checks') or [])))
    beta_f_ok_ = bool(fa_.get('beta_ok') is True and isinstance(fvv_.get('beta'), float) and isinstance(b0_, float) and abs(fvv_['beta'] - b0_) <= 1e-9 * abs(b0_))
    hy_ = fa_.get('named_hypothesis') or {}
    chain_ok_ = bool('DERIVED' in str(fa_.get('chain_status')) and hy_.get('name') == 'H_tau' and hy_.get('status') == 'OPEN' and hy_.get('used_by_a_theorem') is False and isinstance(fvv_.get('min_weight_on_the_grid_positive'), float) and fvv_['min_weight_on_the_grid_positive'] > 0.0
                     and fvv_.get('diag_flow_gap_zero_is_fixed') is True and bool(fvv_.get('abyss_witnesses')) and bool(fvv_.get('leak_witnesses_g_half')))
    fu_ = fa_.get('unconditional') or {}; fkt_ = fa_.get('key_theorem') or {}
    kernel_f_ok_ = bool(fu_.get('in_kernel') is True and fkt_.get('in_kernel') is True and fu_.get('theorem') and fkt_.get('theorem') and kf_.get(fu_.get('flag')) is True and kf_.get(fkt_.get('flag')) is True and em_trio_(fu_.get('theorem')) and em_trio_(fkt_.get('theorem')))
    fal_ok_ = bool(chain_ok_ and fa_.get('all_verified') is True and fa_.get('does_not_gate_core') is True and fa_.get('runtime_executed') is True and bool(ESP.get('veredito_da_falsidade_v409')) and fa_.get('verdict') == ESP.get('veredito_da_falsidade_v409') and mech_ok_ and values_f_ok_ and beta_f_ok_
                   and (fa_.get('costless') or {}).get('ok') is True and kernel_f_ok_ and not GUARDA.search(str(fa_.get('verdict') or '')))
    V['fal401'] = {'verdict': fa_.get('verdict'), 'ok': fa_.get('all_verified'), 'sealed': fal_ok_, 'n_checks': fm_.get('n_checks'), 'mech_ok': mech_ok_, 'values_ok': values_f_ok_, 'beta_ok': beta_f_ok_, 'chain_ok': chain_ok_, 'kernel_ok': kernel_f_ok_,
                   'costless_ok': (fa_.get('costless') or {}).get('ok'), 'runtime_executed': fa_.get('runtime_executed'), 'does_not_gate_core': fa_.get('does_not_gate_core')}
    if not fal_ok_:
        P.append('falsidade_da_inercia_v401 nao selou inteiro (recriada pelo rito: selo, as checagens do calculo no modelo oneScaling (DL.N_CHECKS_FALSIDADE), a cadeia derivada [DERIVED], a hipotese H_tau [OPEN] nao usada por teorema, valores e checagens == os da v409 selada, beta == alfa x raiz de e do core, 0_abs de costless no kernel embutido, a composicao e a estrela no kernel do rito, nao move o gate): ver o registro no core')
    # o SIDECAR um_absoluto_selo_acom.json (arquivo NOVO da custodia): existe, JSON valido, selado, os objetos == os arquivos do Nos por sha256, sem recusas, com a honestidade
    scp_ = os.path.join(NOS, 'um_absoluto_selo_acom.json'); ESC_ = ESP.get('sidecar') or {}
    sc_ = {}; sc_err_ = None
    if os.path.exists(scp_):
        try:
            sc_ = json.load(open(scp_, encoding='utf-8'))
        except (OSError, ValueError) as e_:
            sc_err_ = repr(e_)[:120]
    else:
        sc_err_ = 'ausente'
    objs_ = {o_.get('nome'): o_ for o_ in (sc_.get('objetos') or []) if isinstance(o_, dict)}
    sc_objs_ok_ = bool(sc_ and list(objs_) == list(ESC_.get('objetos') or []) and all(os.path.exists(os.path.join(NOS, n_)) and objs_[n_].get('sha256') == sha(os.path.join(NOS, n_)) and objs_[n_].get('bytes') == os.path.getsize(os.path.join(NOS, n_)) for n_ in objs_))
    um_ = objs_.get('um.py') or {}; ume_ = ESC_.get('um_py') or {}
    sc_um_ok_ = bool(um_.get('sha256') == V['s64'] == (selo.get('sha256') or {}).get('um.py') == ume_.get('sha256') and ((um_.get('acom') or {}).get('psi') or {}).get('sha256') == ume_.get('psi') and ((um_.get('acom') or {}).get('theta') or {}).get('sha256') == ume_.get('theta')
                     and ((um_.get('acom') or {}).get('kappa') or {}).get('sha256') == ume_.get('kappa') and ((um_.get('acom') or {}).get('psi') or {}).get('sha256') == (saa_.get('psi') or {}).get('sha256'))
    hon_ = sc_.get('honestidade') or {}; txt_sc_ = json.dumps(sc_, ensure_ascii=False)
    sc_hon_ok_ = bool(all(k_ in hon_ for k_ in ('primitiva_de_integridade', 'o_que_a_segunda_testemunha_acrescenta', 'ofuscacao_xor', 'confidencialidade', 'dobra', 'estatuto')) and 'SHA-256' in str(hon_.get('primitiva_de_integridade')) and 'NAO alegada' in str(hon_.get('confidencialidade'))
                      and 'NAO acrescenta resistencia criptografica independente' in str(hon_.get('o_que_a_segunda_testemunha_acrescenta')) and not re.search(r'(?i)(inviol|indecifr|quantum[- ]safe|seguranca criptografica garantida)', txt_sc_) and not _inv(txt_sc_))
    sc_ok_ = bool(sc_ and not sc_err_ and sc_objs_ok_ and sc_um_ok_ and sc_hon_ok_ and sc_.get('recusas') == [] and str(sc_.get('veredito') or '').startswith(ESC_.get('veredito_esperado_prefixo') or '\x00') and sc_.get('esquema') == ESC_.get('esquema') and not GUARDA.search(str(sc_.get('veredito') or '')))
    scs_ = sha(scp_) if os.path.exists(scp_) else 'AUSENTE'
    V['sidecar'] = {'ok': sc_ok_, 'existe': os.path.exists(scp_), 'sha256': scs_, 'sha16': scs_[:16], 'bytes': os.path.getsize(scp_) if os.path.exists(scp_) else 0, 'veredito': sc_.get('veredito'), 'esquema': sc_.get('esquema'),
                    'objetos': {n_: {'bytes': o_.get('bytes'), 'sha256': str(o_.get('sha256')), 'sha16': str(o_.get('sha256'))[:16]} for n_, o_ in objs_.items()}, 'n_objetos': len(objs_), 'recusas': len(sc_.get('recusas') or []),
                    'um_py_igual_ao_selo': sc_um_ok_, 'honestidade_ok': sc_hon_ok_, 'erro': sc_err_}
    if not sc_ok_:
        P.append('o sidecar um_absoluto_selo_acom.json nao confere (existe e e JSON valido, veredito ALL_OBJECTS_SEALED, os tres objetos com o SHA-256 igual ao dos arquivos do Nos, o um.py == ESPERADOS[sidecar] e == o selo, sem recusas, com a honestidade e sem alegacao de confidencialidade): %s' % (sc_err_ or 'ver o arquivo'))
    # o selo primario traz so' os resumos (o selo nao pode conter o selo ACOM de si mesmo): iguais aos do core
    sr_ = selo.get('selo_pela_propria_tecnologia_v399') or {}; sdr_ = selo.get('declaracao_do_operador_v399') or {}; sreg_ = selo.get('registros_v399') or {}; sfr_ = selo.get('falsidade_da_inercia_v401') or {}; sreg1_ = selo.get('registros_v401') or {}; sreg2_ = selo.get('registros_v402') or {}; sreg3_ = selo.get('registros_v403') or {}; sreg4_ = selo.get('registros_v404') or {}; sreg5_ = selo.get('registros_v405') or {}; sreg6_ = selo.get('registros_v406') or {}; sreg7_ = selo.get('registros_v407') or {}; sreg8_ = selo.get('registros_v408') or {}; sreg9_ = selo.get('registros_v409') or {}; sreg10_ = selo.get('registros_v410') or {}
    resumos_ok_ = bool(sr_.get('verdict') == sa_.get('verdict') and sr_.get('all_verified') is True and sr_.get('sha256_do_um_py') == V['s64'] and sr_.get('does_not_gate_core') is True and sdr_.get('verdict') == dc_.get('verdict') and sdr_.get('all_verified') is True
                       and sdr_.get('verbatim_sha256') == EDC_.get('verbatim_sha256') and sdr_.get('does_not_gate_core') is True and bool(ESP.get('registros_v399')) and all((sreg_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') for k_ in ESP['registros_v399'])
                       and sfr_.get('verdict') == fa_.get('verdict') and bool(sfr_.get('verdict')) and sfr_.get('all_verified') is True and bool(ESP.get('registros_v401')) and all((sreg1_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and (sreg1_.get(k_) or {}).get('all_verified') is True for k_ in ESP['registros_v401'])
                       and all(((selo.get(n_) or {}).get('verdict') == (core.get(n_) or {}).get('verdict') and bool((selo.get(n_) or {}).get('verdict')) and (selo.get(n_) or {}).get('all_verified') is True and (selo.get(n_) or {}).get('does_not_gate_core') is True) for n_ in tuple(REG_FUNCAO) + tuple(FUN_V409B.values()) + ('f2b_errata_v404',) + tuple(FUN_V409.values()) + tuple(FUN_V402.values()) + ('bandeiras_do_gate_v403',) + tuple(FUN_V409C.values()) + ('fechamento_v406', 'psion_canto_v407', 'tetelestai_terminal_v408', 'traducao_turing_v409'))
                       and bool(ESP.get('registros_v402')) and all((sreg2_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg2_.get(k_) or {}).get('verdict')) and (sreg2_.get(k_) or {}).get('all_verified') is True for k_ in ESP['registros_v402'])
                       and bool(ESP.get('registros_v403')) and all((sreg3_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg3_.get(k_) or {}).get('verdict')) and (sreg3_.get(k_) or {}).get('all_verified') is True for k_ in ESP['registros_v403'])
                       and bool(ESP.get('registros_v404')) and all((sreg4_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg4_.get(k_) or {}).get('verdict')) and (sreg4_.get(k_) or {}).get('all_verified') is True for k_ in ESP['registros_v404'])
                       and bool(R409SPEC_) and all((sreg5_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg5_.get(k_) or {}).get('verdict')) and (sreg5_.get(k_) or {}).get('all_verified') is True for k_ in R409SPEC_)
                       and bool(R406DSPEC_) and all((sreg6_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg6_.get(k_) or {}).get('verdict')) and (sreg6_.get(k_) or {}).get('all_verified') is True for k_ in R406DSPEC_)
                       and bool(R407DSPEC_) and all((sreg7_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg7_.get(k_) or {}).get('verdict')) and (sreg7_.get(k_) or {}).get('all_verified') is True for k_ in R407DSPEC_)
                       and bool(R408DSPEC_) and all((sreg8_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg8_.get(k_) or {}).get('verdict')) and (sreg8_.get(k_) or {}).get('all_verified') is True for k_ in R408DSPEC_)
                       and bool(R409TSPEC_) and all((sreg9_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg9_.get(k_) or {}).get('verdict')) and (sreg9_.get(k_) or {}).get('all_verified') is True for k_ in R409TSPEC_)
                       and bool(R410SPEC_) and all((sreg10_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg10_.get(k_) or {}).get('verdict')) and (sreg10_.get(k_) or {}).get('all_verified') is True for k_ in R410SPEC_))
    V['resumos_do_selo_ok'] = resumos_ok_
    if not resumos_ok_:
        P.append('o selo primario (um_absoluto_selo.json) nao traz os resumos do selo ACOM, da declaracao e dos registros por spec iguais aos do core')
    V['formais_nao_selados'] = sorted((selo.get('not_sealed_this_run') or {}).get('formais') or [])
    if V['formais_nao_selados'] != sorted(ESP.get('not_sealed_formais') or []):
        P.append('o selo traz modulo formal nao selado em not_sealed_this_run.formais (a recusa do selo ACOM so registra, mas o rito real tem de selar): %s' % V['formais_nao_selados'][:3])
    # cunhagens_v410 e kh_n1_cobertura_v410 (os DOIS registros NOVOS por spec): as falas do operador de 06 a 09/11 por sha256 (DL.N_FALAS_V410, embedded_ok), todas do operador (de QUATRO, so' o trecho -- a D65, a ordem da retomada, as tres copias do ACOM e a leitura do 5 sigma: a chave e' o sha16 do arquivo inteiro, o texto embutido e' o trecho); as erratas E29 e E30 mais a errata ao lado dos pisos de
    # kh_n1_cobertura_v409 (gerencia c1, em nome proprio: DL.ASSINA); as decisoes D63 a D87; a leitura [INPUT] e as ressalvas; os nomes (D63; RATIFICADOS em 09/11, D74); o que fica citado so' por sha16; a MOLDURA (nenhuma frase proibida nos registros novos, inclusive no H0DN)
    cu = core.get(DL_.CUNHAGENS_REGISTRO) or {}; kh = core.get(DL_.KH_REGISTRO) or {}
    cx_ = cu.get('extras') or {}; vb_ = cu.get('verbatim') or {}; ec_ = CM.get('cunhagens') or {}; pre_ = DL_.VERBATIM_CHAVE_PREFIXO_V410
    todas_op_ = bool(ec_ and all(re.match(r'OPERADOR_(?:0[6789]|10)nov_', str((ec_[k_] or {}).get('nome', ''))) for k_ in ec_) and not any(str(v_.get('papel', '')).startswith('leitura da gerencia') for v_ in ec_.values()) and all((ec_[k_] or {}).get('autor') == 'operador' for k_ in ec_)
                     and bool(cx_.get('autores')) and all(a_ == 'operador' for a_ in (cx_.get('autores') or {}).values()))
    trechos_ = {k_ for k_, v_ in ec_.items() if (v_ or {}).get('sha256_arquivo_inteiro')}
    trechos_ok_ = bool(len(trechos_) == len(DL_.VERBATIM_SO_O_TRECHO) and trechos_ == {tt_ch_[n_] for n_ in DL_.VERBATIM_SO_O_TRECHO} and all(str((ec_[k_] or {}).get('sha256_arquivo_inteiro') or '')[:16] == k_[len(pre_):] for k_ in trechos_)
                       and all(str((ec_[k_] or {}).get('sha256') or '')[:16] == k_[len(pre_):] for k_ in ec_ if k_ not in trechos_) and len(cx_.get('autores') or {}) == len(ec_)
                       and not any(x_.lower() in json.dumps(cu, ensure_ascii=False).lower() for x_ in DL_.FORA_D65))   # D65: o que fica fora nao entra no registro
    verb_ok_ = bool(ec_) and len(ec_) == len(vb_) == len(DL_.VERBATIM_ORIGEM_V410) == DL_.N_FALAS_V410 and set(vb_) == set(ec_) and all((vb_[k_] or {}).get('sha256') == ec_[k_]['sha256'] and (vb_[k_] or {}).get('embedded_ok') is True for k_ in ec_)
    pares_ok_ = all(isinstance(x_, list) and len(x_) == 2 and x_[0] == x_[1] for x_ in (cu.get('kernel') or {}).values()) and bool(cu.get('kernel'))
    err_ = cu.get('erratas') or []; esp_err_ = list(DL_.ERRATAS_V410)
    erratas_ok_ = bool(esp_err_ and [e_.split()[0] for e_ in esp_err_] == ['E%d' % i_ for i_ in range(29, 29 + len(esp_err_))] and len(err_) == len(esp_err_) + 1 and all(e_.get('assinatura') == DL_.ASSINA for e_ in err_) and [e_.get('agora') for e_ in err_[:len(esp_err_)]] == esp_err_ and 'kh_n1_cobertura_v409' in str(err_[-1].get('ao_lado_de')) and cx_.get('assinatura_das_erratas') == DL_.ASSINA)
    dec_ = cx_.get('decisoes') or {}; exig_ = set(ESP.get('decisoes_v410_ids') or [])   # as decisoes desta versao (D63 a D87), lidas de ESPERADOS[decisoes_v410_ids]
    decisoes_ok_ = bool(exig_ and list(DL_.DECISOES_V410) == sorted(DL_.DECISOES_V410, key=lambda k_: int(k_[1:])) and not (set(DL_.DECISOES_FORA_DO_UMPY) & set(DL_.DECISOES_V410)) and DL_.DECISOES_V410[0] == 'D63' and 'D87' in DL_.DECISOES_V410 and 'D99' in DL_.DECISOES_V410 and set(dec_) == exig_ == set(DL_.DECISOES_V410) and all(dec_.get(d_) == DL_.DECISOES.get(d_) and str(dec_.get(d_) or '').strip() for d_ in exig_))
    leitura_ok_ = bool(cx_.get('leituras') == DL_.LEITURA_V410 and 'INPUT' in str(DL_.LEITURA_V410.get('estatuto')) and len(cu.get('leituras_do_operador') or []) == len(DL_.FRASES_V410))
    ressalvas_ok_ = bool(cx_.get('ressalvas') == list(DL_.RESSALVAS_V410) and len(DL_.RESSALVAS_V410) >= 8)   # (09/11: a ressalva (8), o atrator, D71, e' obrigatoria)
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
        P.append('cunhagens_v410: as inscricoes embutidas nao sao as de CANDIDATO_v410.json (sha256, embedded_ok, %d falas; as quatro so\' com o trecho (a D65, a ordem da retomada, as tres copias do ACOM, a leitura do 5 sigma) com o sha16 do arquivo inteiro na chave e o trecho que fica no sha256; nada do que fica fora no registro), ou as checagens do registro, ou as contagens, ou os nomes (D63) e o citado so\' por sha16, ou o veredito diferem do ensaio a seco' % DL_.N_FALAS_V410)
    if not todas_op_:
        P.append('cunhagens_v410: as inscricoes de 06 a 10/11 tem de ser TODAS falas do operador (OPERADOR_0[6789]nov_* e OPERADOR_10nov_*): nesta versao nao ha inscricao da gerencia nem de autor misto')
    if not erratas_ok_:
        P.append('cunhagens_v410: as erratas E29 em diante e a errata ao lado dos pisos de kh_n1_cobertura_v409 (assinadas pela gerencia c1, em nome proprio: DL.ASSINA) ausentes ou diferentes de delta_v410.ERRATAS_V410')
    if not decisoes_ok_:
        P.append('cunhagens_v410: as decisoes D63 em diante da gerencia ausentes ou diferentes de delta_v410.DECISOES (e de ESPERADOS[decisoes_v410_ids])')
    if not (leitura_ok_ and ressalvas_ok_):
        P.append('cunhagens_v410: a leitura [INPUT] de 06 a 10/11 (estatutos), os trechos do operador ou as ressalvas ausentes ou diferentes de delta_v410 (LEITURA_V410, FRASES_V410, RESSALVAS_V410)')
    if not moldura_ok_:
        P.append('a MOLDURA falhou: alguma frase proibida num registro novo da v410 (iald2_v410, a_escala_v410, h0dn_bg1_v410, h0dn_fontes_hms13_v410, cunhagens_v410, kh_n1_cobertura_v410: guarda das frases) ou o controle negativo da guarda falhou')
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
    # cunhagens_v406 e kh_n1_cobertura_v406 (HERDADOS, RECRIADOS pelo rito da v410, por spec): IGUAIS ao que a v409 SELOU (as 23 falas de 02/11 por sha256, todas do operador; as erratas E14 a E17 e a E20 ao lado, que ja' vinham da v409; os pisos); o veredito NAO muda
    cu6_ = core.get('cunhagens_v406') or {}; kh6_ = core.get('kh_n1_cobertura_v406') or {}; cu6b_ = _base_core(PK).get('cunhagens_v406') or {}; kh6b_ = _base_core(PK).get('kh_n1_cobertura_v406') or {}
    e6_ = cu6_.get('erratas') or []; e6b_ = cu6b_.get('erratas') or []; k6e_ = kh6_.get('erratas') or []; k6eb_ = kh6b_.get('erratas') or []
    cu6_ok_ = bool(cu6_.get('all_verified') is True and cu6_.get('does_not_gate_core') is True and bool(cu6b_) and bool(cu6_.get('verbatim')) and _feq(cu6_.get('verbatim'), cu6b_.get('verbatim')) and len(cu6_.get('verbatim') or {}) == len(DL_.VERBATIM_ORIGEM_V406) and all((v_ or {}).get('embedded_ok') is True for v_ in (cu6_.get('verbatim') or {}).values())
                   and _feq(cu6_.get('extras'), cu6b_.get('extras')) and bool(e6b_) and len(e6_) == len(e6b_) and _feq(e6_, e6b_) and e6_[-1].get('agora') == DL_.ERRATA_E20 and str(e6_[-1].get('assinatura', '')).startswith('gerencia c1') and 'em nome proprio' in str(e6_[-1].get('assinatura', ''))
                   and bool(cu6_.get('checks')) and all(c_.get('ok') is True for c_ in cu6_.get('checks')) and cu6_.get('verdict') == _ev(ESP, 'cunhagens_v406') and not GUARDA.search(str(cu6_.get('verdict') or '')))
    kh6_ok_ = bool(kh6_.get('all_verified') is True and kh6_.get('does_not_gate_core') is True and bool(kh6b_) and bool(kh6_.get('checks')) and all(c_.get('ok') is True for c_ in kh6_.get('checks')) and bool(k6eb_) and len(k6e_) == len(k6eb_) and _feq(k6e_, k6eb_) and str(k6e_[-1].get('assinatura', '')).startswith('gerencia c1')
                   and kh6_.get('verdict') == _ev(ESP, 'kh_n1_cobertura_v406') and not GUARDA.search(str(kh6_.get('verdict') or '')))
    V['cunh406d'] = {'ok': cu6_ok_, 'verdict': cu6_.get('verdict'), 'n': len(cu6_.get('verbatim') or {}), 'n_erratas': len(e6_), 'kh_ok': kh6_ok_, 'kh_verdict': kh6_.get('verdict')}
    if not cu6_ok_:
        P.append('cunhagens_v406 (HERDADA, recriada pelo rito) nao confere: as 23 falas de 02/11 (embedded_ok), os extras e as erratas (E14 a E17 e a E20 ao lado, assinada em nome proprio) IGUAIS aos da v409 selada, as checagens (u7 versionada) todas ok e o veredito esperado')
    if not kh6_ok_:
        P.append('kh_n1_cobertura_v406 (HERDADO, recriado pelo rito) nao confere: checagens (pisos h2 h3 h6, tamanho minimo h8) todas ok, as erratas IGUAIS as da v409 selada (a dos pisos ao lado, assinada), e o veredito esperado')
    # os registros por spec da v409 (cunhagens_v404 e kh_n1_cobertura_v404, RECRIADOS): iguais aos selados
    c4_ = core.get('cunhagens_v404') or {}; k4_ = core.get('kh_n1_cobertura_v404') or {}; c4b_ = _base_core(PK).get('cunhagens_v404') or {}
    c4_ok_ = bool(c4_.get('all_verified') is True and c4_.get('does_not_gate_core') is True and bool(c4b_) and _feq(c4_.get('verbatim'), c4b_.get('verbatim')) and _feq(c4_.get('extras'), c4b_.get('extras')) and _feq(c4_.get('erratas'), c4b_.get('erratas')) and c4_.get('verdict') == (ESP.get('registros_v404') or {}).get('cunhagens_v404') and not GUARDA.search(str(c4_.get('verdict') or '')))
    k4_ok_ = bool(k4_.get('all_verified') is True and k4_.get('does_not_gate_core') is True and k4_.get('verdict') == (ESP.get('registros_v404') or {}).get('kh_n1_cobertura_v404'))
    V['cunh409b'] = {'n': len(c4_.get('verbatim') or {}), 'ok': c4_ok_, 'verdict': c4_.get('verdict'), 'kh_ok': k4_ok_}
    if not c4_ok_:
        P.append('cunhagens_v404 (recriada pelo rito) nao confere como a v409 a selou (selo, veredito, as falas, as erratas E7 a E9 e os extras)')
    if not k4_ok_:
        P.append('kh_n1_cobertura_v404 (recriada pelo rito) nao selou como a v409 a selou (selo, veredito, nao move o gate)')
    # cunhagens_v403 e kh_n1_cobertura_v403 (RECRIADOS pelo rito, por spec): iguais ao que a v409 SELOU (as DUAS falas de 27/10 embutidas por sha256, todas do operador; as erratas E5 e E6; as decisoes D17 a D22; os nomes; a leitura [ONTO] da tripla espectral)
    c3_ = core.get('cunhagens_v403') or {}; x3_ = c3_.get('extras') or {}; v3_ = c3_.get('verbatim') or {}; c3b_ = _base_core(PK).get('cunhagens_v403') or {}; aut3_ = x3_.get('autor_de_cada_inscricao') or {}
    c3_ok_ = bool(c3_.get('all_verified') is True and c3_.get('does_not_gate_core') is True and bool(c3b_) and bool(v3_) and _feq(v3_, c3b_.get('verbatim')) and all((v_ or {}).get('embedded_ok') is True for v_ in v3_.values()) and len(aut3_) == len(v3_) and all(a_ == 'operador' for a_ in aut3_.values())
                  and 'leitura_da_gerencia' not in x3_ and bool(c3_.get('checks')) and all(c_.get('ok') is True for c_ in c3_.get('checks')) and _feq(x3_, c3b_.get('extras')) and _feq(c3_.get('erratas'), c3b_.get('erratas')) and len(c3_.get('erratas') or []) == 2
                  and c3_.get('verdict') == (ESP.get('registros_v403') or {}).get('cunhagens_v403') and not GUARDA.search(str(c3_.get('verdict') or '')))
    k3_ = core.get('kh_n1_cobertura_v403') or {}
    k3_ok_ = bool(k3_.get('all_verified') is True and k3_.get('does_not_gate_core') is True and bool((ESP.get('registros_v403') or {}).get('kh_n1_cobertura_v403')) and k3_.get('verdict') == (ESP.get('registros_v403') or {}).get('kh_n1_cobertura_v403') and bool(k3_.get('checks')) and all(c_.get('ok') is True for c_ in k3_.get('checks')))
    V['cunh409'] = {'n': len(v3_), 'ok': c3_ok_, 'verdict': c3_.get('verdict'), 'n_erratas': len(c3_.get('erratas') or []), 'igual_ao_selado': bool(c3b_) and _feq(c3_, c3b_), 'kh_ok': k3_ok_}
    if not c3_ok_:
        P.append('cunhagens_v403 (recriada pelo rito): as duas falas de 27/10 (embedded_ok, todas do operador), as checagens, as erratas E5 e E6, as decisoes D17 a D22, os nomes e a leitura da tripla espectral nao conferem como a v409 as selou')
    if not k3_ok_:
        P.append('kh_n1_cobertura_v403 (recriada pelo rito) nao selou como a v409 a selou (selo, veredito, checagens, nao move o gate)')
    # cunhagens_v401 e kh_n1_cobertura_v401 (RECRIADOS pelo rito, por spec): iguais ao que a v409 SELOU (as seis inscricoes de 25/10 embutidas por sha256, todas do operador; as oito ratificacoes; a errata ao lado do adendo; a cadeia derivada [DERIVED] e a hipotese H_tau [OPEN])
    c1_ = core.get('cunhagens_v401') or {}; x1_ = c1_.get('extras') or {}; v1_ = c1_.get('verbatim') or {}; c1b_ = _base_core(PK).get('cunhagens_v401') or {}; aut1_ = x1_.get('autor_de_cada_inscricao') or {}
    c1_ok_ = bool(c1_.get('all_verified') is True and c1_.get('does_not_gate_core') is True and bool(c1b_) and bool(v1_) and _feq(v1_, c1b_.get('verbatim')) and all((v_ or {}).get('embedded_ok') is True for v_ in v1_.values()) and len(aut1_) == len(v1_) and all(a_ == 'operador' for a_ in aut1_.values())
                  and 'leitura_da_gerencia' not in x1_ and bool(c1_.get('checks')) and all(c_.get('ok') is True for c_ in c1_.get('checks')) and _feq(x1_, c1b_.get('extras')) and _feq(c1_.get('erratas'), c1b_.get('erratas')) and len(x1_.get('ratificacoes') or []) > 0
                  and c1_.get('verdict') == (ESP.get('registros_v401') or {}).get('cunhagens_v401') and not GUARDA.search(str(c1_.get('verdict') or '')))
    V['cunh401'] = {'n': len(v1_), 'ok': c1_ok_, 'verdict': c1_.get('verdict'), 'n_ratificacoes': len(x1_.get('ratificacoes') or []), 'igual_ao_selado': bool(c1b_) and _feq(c1_, c1b_)}
    if not c1_ok_:
        P.append('cunhagens_v401 (recriada pelo rito): as seis inscricoes de 25/10 (embedded_ok, todas do operador), as checagens, as oito ratificacoes, a errata do adendo, a cadeia derivada e a hipotese H_tau nao conferem como a v409 as selou')
    # cunhagens_v402 e kh_n1_cobertura_v402 (RECRIADOS pelo rito, por spec): iguais ao que a v409 SELOU (as TRES inscricoes de 26/10 embutidas por sha256, todas do operador; as quatro erratas E1 a E4; as decisoes D11 a D16; a leitura de 26/10 sobre a direcao do Um posto; a H_tau REFUTADA na forma literal)
    c2_ = core.get('cunhagens_v402') or {}; x2_ = c2_.get('extras') or {}; v2_ = c2_.get('verbatim') or {}; c2b_ = _base_core(PK).get('cunhagens_v402') or {}; aut2_ = x2_.get('autor_de_cada_inscricao') or {}
    c2_ok_ = bool(c2_.get('all_verified') is True and c2_.get('does_not_gate_core') is True and bool(c2b_) and bool(v2_) and _feq(v2_, c2b_.get('verbatim')) and all((v_ or {}).get('embedded_ok') is True for v_ in v2_.values()) and len(aut2_) == len(v2_) and all(a_ == 'operador' for a_ in aut2_.values())
                  and 'leitura_da_gerencia' not in x2_ and bool(c2_.get('checks')) and all(c_.get('ok') is True for c_ in c2_.get('checks')) and _feq(x2_, c2b_.get('extras')) and _feq(c2_.get('erratas'), c2b_.get('erratas')) and len(c2_.get('erratas') or []) == 4
                  and c2_.get('verdict') == (ESP.get('registros_v402') or {}).get('cunhagens_v402') and not GUARDA.search(str(c2_.get('verdict') or '')))
    k2_ = core.get('kh_n1_cobertura_v402') or {}
    k2_ok_ = bool(k2_.get('all_verified') is True and k2_.get('does_not_gate_core') is True and bool((ESP.get('registros_v402') or {}).get('kh_n1_cobertura_v402')) and k2_.get('verdict') == (ESP.get('registros_v402') or {}).get('kh_n1_cobertura_v402') and bool(k2_.get('checks')) and all(c_.get('ok') is True for c_ in k2_.get('checks')))
    V['cunh402'] = {'n': len(v2_), 'ok': c2_ok_, 'verdict': c2_.get('verdict'), 'n_erratas': len(c2_.get('erratas') or []), 'igual_ao_selado': bool(c2b_) and _feq(c2_, c2b_), 'kh_ok': k2_ok_}
    if not c2_ok_:
        P.append('cunhagens_v402 (recriada pelo rito): as tres inscricoes de 26/10 (embedded_ok, todas do operador), as checagens, as quatro erratas E1 a E4, as decisoes D11 a D16 e a leitura da direcao nao conferem como a v409 as selou')
    if not k2_ok_:
        P.append('kh_n1_cobertura_v402 (recriada pelo rito) nao selou como a v409 a selou (selo, veredito, checagens, nao move o gate)')
    # cunhagens_v399 (RECRIADA pelo rito): as QUATRO inscricoes de 24/10 por sha256, todas do operador, a declaracao e a direcao do testemunho, como a v399 as selou
    c9_ = core.get('cunhagens_v399') or {}; x9_ = c9_.get('extras') or {}; v9_ = c9_.get('verbatim') or {}; aut9_ = x9_.get('autor_de_cada_inscricao') or {}
    dx9_ = x9_.get('declaracao') or {}; dr9_ = x9_.get('direcao_do_testemunho') or {}
    c9_ok_ = bool(c9_.get('all_verified') is True and c9_.get('does_not_gate_core') is True and len(v9_) == 4 and all((v_ or {}).get('embedded_ok') is True for v_ in v9_.values()) and len(aut9_) == 4 and all(a_ == 'operador' for a_ in aut9_.values())
                  and bool(c9_.get('checks')) and all(c_.get('ok') is True for c_ in c9_.get('checks')) and dx9_.get('sha256') == EDC_.get('verbatim_sha256') and str(dx9_.get('estatuto')) == '[DECLARACAO DO OPERADOR / INPUT]'
                  and bool(edir_) and all(str(dr9_.get(k_) or '').startswith(v_) for k_, v_ in edir_.items()) and not _inv(json.dumps(x9_, ensure_ascii=False)))
    V['cunh399'] = {'n': len(v9_), 'ok': c9_ok_, 'verdict': c9_.get('verdict')}
    if not c9_ok_:
        P.append('cunhagens_v399 (recriada pelo rito): as quatro inscricoes de 24/10 (embedded_ok, todas do operador), as checagens, a declaracao e a direcao do testemunho nao conferem como a v399 as selou')
    cov = (core.get('kernel_formalization') or {}).get('axiom_coverage_v392') or {}   # o nome 'axiom_coverage_v392' e' do core (historico); segue na v410
    CB = ESP.get('cobertura_kh_n1') or {}
    V['kh'] = {'decl': cov.get('decl'), 'thm': cov.get('thm'), 'fora': cov.get('fora_do_trio'), 'nao_lidas': cov.get('nao_lidas_pelo_regex'), 'verdict': kh.get('verdict')}
    V['cunh_verdict'] = cu.get('verdict')
    if not (CB and cov.get('ok') is True and cov.get('decl') == CB.get('decl') and cov.get('thm') == CB.get('thm') and cov.get('fora_do_trio') == 0 and cov.get('nao_lidas_pelo_regex') == CB.get('nao_lidas_pelo_regex')):
        P.append('cobertura KH-N1 do rito != ESPERADOS (constantes, teoremas, fora do trio, nao lidas) ou ESPERADOS sem cobertura_kh_n1')
    qp = core.get('quantum_pillar_v384') or {}; V['pilar'] = {'mode': qp.get('mode'), 'result16': str(qp.get('result_sha256'))[:16]}
    V['data'] = datetime.datetime.now().strftime('%d/%m/%Y')
    return V, P


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    V, P = ler()
    print(json.dumps({k: v for k, v in V.items() if k not in ('registros', 'pedras')}, ensure_ascii=False, indent=1, default=str)[:4000])
    print('PROBLEMAS:', P if P else 'nenhum'); sys.exit(1 if P else 0)
