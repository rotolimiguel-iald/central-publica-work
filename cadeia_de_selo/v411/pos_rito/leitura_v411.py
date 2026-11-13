# -*- coding: utf-8 -*-
# [ADAPTADO v411, 12/11/2026, claude-sonnet-posrito-L-v411, a servico do claude-construtor-v411] a leitura da rodada v411: o TESTE H0DN x BG1 ABERTO UMA VEZ (D169) e o resultado RECALCULADO no rito; NENHUM modulo novo de kernel (o kernel e a escada sao os da v410, lidos e conferidos como ZERO modulo e ZERO bandeira nova);
# UM registro novo com FUNCAO (h0dn_bg1_v411, 16 checagens; V['fecho']: as DUAS linhas, os atos, as sete ressalvas, o que o teste nao decide) e DOIS por spec (cunhagens_v411: as falas de 11 e 12/11 e as decisoes do delta, E41 a E43 e a errata dos pisos; kh_n1_cobertura_v411); os QUATRO registros com funcao da v410
# (iald2_v410, a_escala_v410, h0dn_bg1_v410, h0dn_fontes_hms13_v410) e os DOIS por spec da v410 (cunhagens_v410, kh_n1_cobertura_v410, este com a errata dos pisos ao lado) sao RECRIADOS no mesmo ponto do main e seguem selados, com o veredito da v410 selada (V['reg410_recriados']; nao sao novos).
# A LEITURA da rodada v411 (molde: leitura_v410.py, que vem de leitura_v407.py, de leitura_v405.py, de leitura_v401.py e de leitura_v399.py FINAL): SO LEITURA do Nos e da pasta da cadeia (work/cadeia_de_selo/v411, que aqui e' o proprio pacote).
# Devolve (V, PROBLEMAS); PROBLEMAS nao vazio => a cadeia PARA. Nenhum numero e' digitado: tudo sai dos JSON, do core, do selo, do sidecar e do stdout do rito; os vereditos e os valores esperados da rodada sao LIDOS de ESPERADOS_v411.json, de CANDIDATO_v411.json e de delta_v411.
# ESPERADOS (chaves lidas aqui; ausente => PROBLEMA, fail-closed): candidato_sha16, origem_sha16, escada, escada_v410_e_v411, vereditos_v410 (os vereditos de TODOS os registros do core da v410 selada), vereditos_novos_v411 (os TRES novos: h0dn_bg1_v411, cunhagens_v411, kh_n1_cobertura_v411), registros_funcao_v411.h0dn
# ({nome, verdict, values, n_checks}; o ensaio a seco), troca_dita, veredito_da_troca_no_ensaio, qg_closure_verdict, qg_closure_gate_verdict_v410, h8_entradas, h8_residuais_do_nos, cobertura_kh_n1, flags_true_v410, selo_acom, declaracao, sidecar.objetos, veracidade, kernel.modulos_novos (0), bundle_sha256 (vazio ou ausente).
# O GATE NAO SE MOVE: o qg_closure do core e' IDENTICO ao da v410. O SIDECAR um_absoluto_selo_acom.json e' lido aqui. A DIRECAO DO TESTEMUNHO segue conferida. As falas de 11 e 12/11 sao TODAS do operador.
# O QUADRO «O Teste da Unica Palavra» (v397) segue selado e igual. As linhas `[v399]` a `[v410]` do stdout (recriadas; os textos sao os que o um.py imprime: a [v408] diz «da v408», a [v409] «da v409», a [v410] «da v410») e a nova `[v411]` dizem os vereditos.
# A linha final do rito: o main imprime, por ultimo, a linha do sidecar (`[selo_acom] ... ALL_OBJECTS_SEALED ; objetos 3 ; recusas 0`), logo depois da do colapso tipado; a leitura exige as DUAS, nessa ordem.
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CONTRATO COM textos_v411.py e fechar_v411.py ("reg410c", "fun410c", "pedras_v408", "cunh410c" etc. sao NOMES HERDADOS do molde e continuam a significar os registros/pedras da v405 selada, recriados):
#   V['n_pedras'] = 0 (nenhum modulo novo) e V['pedras'] = []; V['bandeiras'] {'n': 0, 'n_true': 0, 'ok', 'iguais_a_v410': {...}}; V['ancoras'] e V['ancoras_aescala'] = {} (nenhuma ancora nova);
#   V['fecho'] o registro DESTA versao, h0dn_bg1_v411 {'registro','verdict','ok','sealed','n_checks','mech_ok','values_ok','beta_ok','runtime_executed','does_not_gate_core','opened_once','observed_vector_read','cabeca_do_teste','outcome','primario','cefeidas_livres','linha_ao_lado_cefeidas_livres','lei_em_km_s_Mpc','atos',
#       'ressalvas' (as 7), 'rotulos_das_ressalvas', 'nao_decide' (as 5), 'ressalvas_da_gerencia', 'n_insumos', 'insumos_sha16', 'veredito_montado','stdout_ok','selo_ok','guarda_ok','ressalvas_ok','duas_linhas_ok','gate_ok','emenda_ok','esperado_ok','finitude_ok','escada'};
#   V['reg410_recriados'] DICT nome -> {'verdict','ok','sealed','n_checks','igual_ao_core_da_v410'} dos QUATRO com funcao e DOIS por spec da v410, RECRIADOS (+ 'kh_n1_cobertura_v410'.'errata_dos_pisos');
#   V['fecho410'] o registro HERDADO traducao_turing_v409 (recriado); V['fecho408'] o HERDADO tetelestai_terminal_v408; V['fecho407'] o HERDADO psion_canto_v407 (V['chaves407']); V['fecho406'] o HERDADO fechamento_v406 (V['chaves406']);
#   V['ancoras410'] as da IALD2 e da AEscala (v410); V['ancoras409'] as da traducao; V['ancoras408'] as do terminal; V['ancoras407'] as do psion; V['ancoras406'] as do fechamento (todas lidas do delta, nao do ESPERADOS);
#   V['bundle410'] {'n'(2),'n_ok','ok'}; V['bundle409'] (2); V['bundle408'] (4); V['bundle407'] (9); V['bundle406'] (301) (os sha256 pinados dos deltas, conferidos no kernel do Nos e no hash formal do rito); V['bandeiras410'] (as bandeiras True da v410 selada, todas True);
#   V['reg411'] DICT nome -> {'verdict','ok'} dos TRES registros NOVOS (h0dn_bg1_v411, cunhagens_v411, kh_n1_cobertura_v411); V['registros_novos'] = esses nomes (sorted); V['reg410t'] DICT dos TRES da v409 HERDADOS; V['reg408d'] dos TRES da v408; V['reg407d'] dos da v407; V['reg406d'] dos da v406;
#   V['cunhagens'] (cunhagens_v411) {'n'(DL.N_FALAS_V411),'ok','verbatim_ok','todas_do_operador','erratas_ok','n_erratas'(len(DL.ERRATAS_V411) + 1: E41, E42, E43 e a dos pisos),'decisoes_ok','n_decisoes'(len(DL.DECISOES_V411): as decisoes do delta),'ressalvas_ok','kernel_ok','checks_ok','n_checks','moldura_ok','kh_ok','verdict'};
#   V['cunh410t'] (cunhagens_v409 e kh_n1_cobertura_v409 herdados, kh com os pisos ao lado); V['cunh408d'] (cunhagens_v408 e kh_n1_cobertura_v408 iguais); V['cunh407d'] (iguais); V['cunh406d']; V['kh'] (kh_n1_cobertura_v411) {'decl','thm','fora','nao_lidas',...}
# (as linhas de stdout a conferir: o bloco `H0DN x BG1 ABERTO [v411 ...` seguido de `  primario (modelo publicado): Z nulo = a ; Z K = b ; ramo n  ||  Cefeidas livres (ao lado, no mesmo item): Z nulo = c ; Z K = d ; ramo m  ||  checagens ok = 16/16 ; gate = o mesmo da base` e de `  >>> veredito <<<`;
#  a linha `   [v411] o registro com funcao e os por spec da v411: h0dn_bg1_v411=SELOU | specs: 2 (selados 2)`; a linha RECRIADA `   [v410] os registros com funcao e os por spec da v410: iald2_v410=SELOU | a_escala_v410=SELOU | h0dn_bg1_v410=SELOU | h0dn_fontes_hms13_v410=SELOU | specs: 2 (selados 2)`;
#  a da traducao HERDADA: `   [v409] o registro da traducao e os registros por spec da v409: traducao_turing=SELOU | specs: 2 (selados 2)` e o bloco `A TRADUCAO AS CLASSES DE TURING [v409 ...`; a do terminal HERDADO: `   [v408] ...`; a do psion HERDADO: `   [v407] ...`; a do fechamento HERDADO: `   [v406] ...`.)
import glob, hashlib, json, os, re, sys, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
PK = os.path.dirname(HERE)            # work\cadeia_de_selo\v411
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
FINAL_RE = re.compile(r'^\[selo\] colapso tipado: ')
TRAILER_RE = re.compile(r'^(exit=\d+|rc=\d+|RITO_RC=\S+|inicio |fim )')
GUARDA = re.compile('(?<!NOT_)(?<!UN)' + 'CONF' + 'IRMED|(?<!AP)PRO' + 'VED_BY|TGL_PRO' + 'VED')
REG_V393 = ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393", "kh_n1_cobertura_v393")   # da v393: seguem no core e seguem selados (nao sao 'novos' da v411)
REG_V394 = ("tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394", "criterio_binario_de_parada_v394")   # da v394: seguem no core e seguem selados (nao sao 'novos' da v411)
REG_V395 = ("psibit_v395", "cunhagens_v395", "kh_n1_cobertura_v395")   # da v395: seguem no core e seguem selados (nao sao 'novos' da v411)
REG_V396 = ("testemunha_estatica_v396", "cunhagens_v396", "kh_n1_cobertura_v396")   # da v396: seguem no core e seguem selados (nao sao 'novos' da v411)
REG_V397 = ("teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397")   # da v397 (o Teste da Unica Palavra, a pedra Token e as falas de 23/10): seguem no core e seguem selados; o quadro do topo le o primeiro
REG_V398 = ("sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398")   # da v398 (o sonico, a afinacao das cordas e as falas de 23/10): seguem no core e seguem selados (nao sao 'novos' da v411)
REG_V401 = ("falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401")   # os TRES registros da v401: RECRIADOS pelo rito da v411 (o primeiro com FUNCAO), tem de seguir selados e iguais ao ensaio a seco (e a v410 selada)
REG_V402 = ("ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402")   # os CINCO registros da v402 (tres com FUNCAO, dois por spec): RECRIADOS pelo rito da v411, tem de seguir selados e iguais ao ensaio a seco (e a v410 selada)
REG_V410 = ("caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "cunhagens_v403", "kh_n1_cobertura_v403")   # os SEIS registros da v410 (quatro com FUNCAO, dois por spec): RECRIADOS pelo rito da v411, tem de seguir selados e iguais ao ensaio a seco (e a v410 selada)
REG_V399 = ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399")   # os QUATRO registros da v399: RECRIADOS pelo rito da v411 (os dois primeiros com FUNCAO), tem de seguir selados e iguais ao ensaio a seco
FUN_V402 = {"ponte": "ponte_da_escala_dual_v402", "queda": "queda_sem_geometria_v402", "esperanca": "esperanca_condicional_v402"}   # os TRES registros com FUNCAO da v402 (recriados)
FUN_V410 = {"caminho": "caminho_v403", "vida": "vida_v403", "verdade_adendo": "verdade_adendo_v403"}   # os TRES registros com FUNCAO das pedras da v410 (recriados); o quarto, bandeiras_do_gate_v403, e' lido a parte (V['gate'])
REG_V410B = ("projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "cunhagens_v404", "kh_n1_cobertura_v404")   # os CINCO registros da v410 SELADA: RECRIADOS pelo rito da v411, tem de seguir selados e iguais ao ensaio a seco (e a v410 selada)
FUN_V410B = {"projecao": "projecao_transversal_v404", "jo8v32": "jo8v32_v404"}   # os DOIS registros com FUNCAO das pedras da v410 (recriados); a errata de F2b e' lida a parte (V['f2b'])
REG_FUNCAO = ("h0dn_bg1_v411",)   # o UNICO registro NOVO com FUNCAO, na ordem de delta_v411.REGISTROS_FUNCAO: o teste H0DN x BG1 aberto uma vez (D169)
REG_FIXOS = REG_FUNCAO + ("cunhagens_v411", "kh_n1_cobertura_v411")   # os TRES registros NOVOS do core v411 (um com FUNCAO, dois por spec)
REG_SPEC_V411 = REG_FIXOS[len(REG_FUNCAO):]   # os DOIS por spec novos (cunhagens_v411 e kh_n1_cobertura_v411): os que o selo resume em registros_v411 e que a linha [v411] do stdout conta
REG_RECRIADOS_V410F = ("iald2_v410", "a_escala_v410", "h0dn_bg1_v410", "h0dn_fontes_hms13_v410")   # os QUATRO registros com FUNCAO da v410: RECRIADOS no mesmo ponto do main, selados; NAO sao novos
REG_RECRIADOS_V410S = ("cunhagens_v410", "kh_n1_cobertura_v410")   # os DOIS por spec da v410: RECRIADOS, selados (o kh com a errata dos pisos ao lado)
REG_RECRIADOS_V410 = REG_RECRIADOS_V410F + REG_RECRIADOS_V410S
H0_SELO_CHAVES = ("verdict", "all_verified", "cabeca_do_teste", "outcome", "linha_ao_lado_cefeidas_livres", "observed_vector_read", "opened_once", "runtime_executed", "does_not_gate_core", "n_checks_esperadas", "lei", "modelos", "p2_ao_lado_da_v387")   # o resumo do h0dn_bg1_v411 no selo (13 chaves: a 13a, p2_ao_lado_da_v387, e o aditivo do P2 de 12/11, no registro e no selo) (gerar_candidato_v411.py: N02_selo)
H0_VALUES_COMPARADOS = ("K", "log10K", "beta", "z_star", "Omega_m", "Omega_r", "lei_em_km_s_Mpc", "primario", "cefeidas_livres", "support_l2", "estresse", "coerencia", "esperado_pelos_agregados", "atos", "gate_verdict", "escada", "veredito_montado")   # o que o ensaio a seco e o rito tem de dar IGUAL (nada de caminhos nem tempos)
REG_V410T = ("traducao_turing_v409", "cunhagens_v409", "kh_n1_cobertura_v409")   # os TRES registros da v410 (um com FUNCAO, dois por spec): HERDADOS, RECRIADOS pelo rito da v411 (o main segue rodando o bloco da traducao), selados
REG_V408D = ("tetelestai_terminal_v408", "cunhagens_v408", "kh_n1_cobertura_v408")   # os TRES registros da v408 (um com FUNCAO, dois por spec): HERDADOS, RECRIADOS pelo rito da v411 (o main segue rodando o bloco do terminal), selados
REG_V407D = ("psion_canto_v407", "cunhagens_v407", "kh_n1_cobertura_v407")   # os TRES registros da v407 (um com FUNCAO, dois por spec): HERDADOS, RECRIADOS pelo rito da v411, selados; o psion carrega a escada (troca dita); cunhagens_v407 ganha AO LADO a errata da D57(d) (o pino do acervo da v407 na copia purgada); kh_n1_cobertura_v407 segue igual a v410 selada
REG_V406D = ("fechamento_v406", "cunhagens_v406", "kh_n1_cobertura_v406")   # os TRES registros da v406 (um com FUNCAO, dois por spec): HERDADOS, RECRIADOS pelo rito da v411 (o main segue rodando o bloco do fechamento), selados e de veredito igual ao da v410 selada; as checagens c8 / u7 / h2 h3 h6 h8 sao VERSIONADAS pela errata E20
FUN_V410C = {"ponte": "ponte_da_massa_v405", "tensao": "massa_tensao_pura_v405", "identidade": "identidade_v405", "observador": "observador_terminal_v405", "diminuto": "lei_do_diminuto_v405", "tonica": "tonica_do_hamiltoniano_v405", "disco": "disco_de_euler_v405", "psion": "ponto_zero_do_psion_v405"}   # os OITO registros com FUNCAO da v410 SELADA (um por pedra): RECRIADOS pelo rito da v411
REG_V410C = tuple(FUN_V410C.values()) + ("cunhagens_v405", "campos_fechados_e_leituras_v405", "ga_reclassificacao_v405", "gap_v405", "kh_n1_cobertura_v405")   # os TREZE registros da v410 SELADA (oito com FUNCAO, cinco por spec): RECRIADOS pelo rito da v411 (o main da v410 segue rodando), selados e iguais a v410 selada
SIDECAR_RE = re.compile(r'^\[selo_acom\] (TGL_SELO_ACOM_SIDECAR_V399__ALL_OBJECTS_SEALED\S*) ; objetos (\d+) ; recusas (\d+)$')   # a linha que o main da v411 imprime por ultimo (selo_acom_sidecar_v399)
_RX_INV = re.compile(r'IALD\s+testifica\s+(?:a\s+mim|do\s+operador|de\s+mim)')   # a DIRECAO invertida (a IALD como quem testifica DO operador); so' a fala em que ele a recusa escapa
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()


def _mod_lean(rel):
    """'TGLExt/AEscala.lean' -> 'TGLExt.AEscala' (o nome do modulo como o FLAGS_v411.json o grava; nada digitado)."""
    return 'TGLExt.' + rel[len('TGLExt/'):-len('.lean')].replace('/', '.')


def _quadro_do_pacote(pk_):
    """O quadro_v397 DESTE pacote, carregado pelo CAMINHO (nunca pela ordem do sys.path: um modulo herdado poe a pasta da versao anterior na frente, e la' ha' outra copia de quadro_v397.py, que importa o delta dela)."""
    import importlib.util as _ilu_q
    alvo_ = os.path.normcase(os.path.abspath(os.path.join(pk_, "quadro_v397.py")))
    for nome_ in ("quadro_v397", "quadro_v397__pacote_v411"):
        m_ = sys.modules.get(nome_)
        if m_ is not None and os.path.normcase(os.path.abspath(getattr(m_, "__file__", "") or "")) == alvo_:
            return m_
    if pk_ not in sys.path:
        sys.path.insert(0, pk_)
    sp_ = _ilu_q.spec_from_file_location("quadro_v397__pacote_v411", alvo_); m_ = _ilu_q.module_from_spec(sp_); sp_.loader.exec_module(m_)
    assert getattr(m_.DL, "UM_VERSION", None) == "v411", ("o quadro do pacote nao importou o delta da v411", getattr(m_.DL, "__file__", None))
    sys.modules["quadro_v397__pacote_v411"] = m_
    return m_


def _esp_rf(ESP, curto, completo):
    """O registro com FUNCAO de ESPERADOS[registros_funcao_v411] (o ensaio a seco): pela chave curta (iald2, a_escala, h0dn, hms13) ou pelo nome inteiro do registro; ausente => {} (o chamador RECUSA: fail-closed)."""
    rf_ = ESP.get('registros_funcao_v411') or {}
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
    """O core da v410 SELADA (copia de bytes em PK/base_v410): de onde saem o teorema e o modulo da face de Fock da testemunha (nenhum nome digitado); lido uma vez por caminho."""
    p = os.path.join(pk, 'base_v410', 'um_absoluto.json')
    if p not in _BASE_CORE:
        _BASE_CORE[p] = json.load(open(p, encoding='utf-8'))['core']
    return _BASE_CORE[p]


def _res_path(ev):
    """O resultado pinado do Teste da Unica Palavra: a copia em PK/insumos/fase9 (so' existe no SANDBOX do harness) ou, no real, a copia duravel da v397 (ESPERADOS[veracidade][resultado][duravel]); o sha256 e' conferido contra ESPERADOS em ambos."""
    nome = os.path.basename((ev.get('resultado') or {}).get('duravel') or 'ausente')
    loc = os.path.join(PK, 'insumos', 'fase9', nome)
    return loc if os.path.exists(loc) else ((ev.get('resultado') or {}).get('duravel') or loc)
def _ev(ESP, n_):
    """O veredito ESPERADO de um registro (nada digitado): os NOVOS da v411 sao os do ensaio a seco (ESPERADOS[vereditos_novos_v411]); os que a TROCA DITA muda (so' numeros, mais o veredito dito de rede_fock_v394) sao os do ensaio (ESPERADOS[veredito_da_troca_no_ensaio]);
    os demais sao os da v410 SELADA (ESPERADOS[vereditos_v410], lidos do core de base_v410)."""
    nv_ = ESP.get('vereditos_novos_v411') or {}
    if n_ in nv_:
        return nv_[n_]
    if n_ in (ESP.get('troca_dita') or []):
        return (ESP.get('veredito_da_troca_no_ensaio') or {}).get(n_)
    return (ESP.get('vereditos_v410') or {}).get(n_)




def _ler_fecho_v411(core, ESP, CM, selo, out_n_, DL_, GFH_, P18H_, b0_):
    """Le o registro com FUNCAO h0dn_bg1_v411 (o teste H0DN x BG1 aberto uma vez, RECALCULADO no rito) do core do Nos, FAIL-CLOSED, e devolve (V['fecho'], PROBLEMAS). Confere: selou e foi aberto uma vez; o veredito de maquina == ESPERADOS[vereditos_novos_v411] (prefixo e sufixo do delta);
    as DL.N_CHECKS_FECHO (16) checagens c1..cN todas ok; as DUAS linhas (primario e Cefeidas livres) nos values, cada uma com o seu ramo, e no veredito; os valores == ESPERADOS[registros_funcao_v411][h0dn] (o ensaio a seco), a tolerancia de _feq; o beta == alfa x raiz de e do core; as sete ressalvas e o que o teste nao decide no registro;
    a emenda as claras (a, b, c) e o recalculo igual a abertura (c6, c9 sem divergencias); a guarda de finitude; o gate e a escada da v410; o texto do registro limpo (P18 e guarda das frases; nenhum token proibido; a frase velha da v410 «nenhum dado observado lido» ausente); o bloco do stdout (as duas linhas e o veredito); o resumo no selo."""
    P = []
    h_ = core.get(DL_.FECHO_REGISTRO) or {}; m_ = h_.get('mechanics') or {}; chk_ = m_.get('checks') or []; v_ = h_.get('values') or {}
    E_ = _esp_rf(ESP, 'h0dn', DL_.FECHO_REGISTRO); s_ = selo.get(DL_.FECHO_REGISTRO) or {}; p_ = v_.get('primario') or {}; c_ = v_.get('cefeidas_livres') or {}
    ver_ = str(h_.get('verdict') or ''); ev_ = _ev(ESP, DL_.FECHO_REGISTRO)
    if not (E_ and E_.get('values')):
        P.append('ESPERADOS_v411.json nao traz registros_funcao_v411.h0dn (com verdict, n_checks e values do ensaio a seco; o gerar_esperados_v411 ainda nao o emite): nao ha com que conferir o registro h0dn_bg1_v411 (fail-closed)')
    sel_ok_ = bool(h_.get('all_verified') is True and h_.get('does_not_gate_core') is True and h_.get('runtime_executed') is True and h_.get('opened_once') is True and ver_ and not GUARDA.search(ver_))
    ver_ok_ = bool(ev_ and ver_ == ev_ == (E_ or {}).get('verdict', ev_) and ver_.startswith(DL_.VEREDITO_OK_PREFIXO) and ver_.endswith(DL_.VEREDITO_SUFIXO))
    mech_ok_ = bool(m_.get('passed') is True and m_.get('n_checks') == DL_.N_CHECKS_FECHO == (E_ or {}).get('n_checks', DL_.N_CHECKS_FECHO) == len(chk_) and all(c1_.get('ok') is True for c1_ in chk_) and [c1_.get('id') for c1_ in chk_] == ['c%d' % i_ for i_ in range(1, DL_.N_CHECKS_FECHO + 1)])
    chaves_p_ = ('z_null', 'z_tgl', 'D', 'p_unilateral', 'ramo', 'outcome', 'cabeca_do_teste', 't', 'modelo'); chaves_c_ = ('z_null', 'z_tgl', 'D', 'ramo', 'outcome', 't', 'modelo')
    import math as _m
    duas_ok_ = False
    try:
        duas_ok_ = bool(all(k_ in p_ for k_ in chaves_p_) and all(k_ in c_ for k_ in chaves_c_) and p_['cabeca_do_teste'] == h_.get('cabeca_do_teste') and p_['outcome'] == h_.get('outcome') and (h_.get('linha_ao_lado_cefeidas_livres') or {}).get('ramo') == c_['ramo']
                        and 'PRIMARY_' in ver_ and 'BESIDE_FREE_CEPHEIDS_' in ver_ and ('BRANCH_%s' % p_['ramo']) in ver_ and ('BRANCH_%s' % c_['ramo']) in ver_ and ('%dSIGMA_AGAINST_THE_NULL' % int(_m.floor(float(p_['z_null'])))) in ver_
                        and all(isinstance(p_[k_], float) and _m.isfinite(p_[k_]) for k_ in ('z_null', 'z_tgl', 'D', 'p_unilateral', 't')) and all(isinstance(c_[k_], float) and _m.isfinite(c_[k_]) for k_ in ('z_null', 'z_tgl', 'D', 't')))
    except (TypeError, ValueError, KeyError):
        duas_ok_ = False
    ev_values_ = (E_ or {}).get('values') or {}
    esp_ok_ = bool(ev_values_ and all(k_ in v_ for k_ in H0_VALUES_COMPARADOS if k_ in ev_values_) and _feq({k_: v_.get(k_) for k_ in H0_VALUES_COMPARADOS if k_ in ev_values_}, {k_: ev_values_[k_] for k_ in H0_VALUES_COMPARADOS if k_ in ev_values_}))
    beta_ok_ = bool(h_.get('beta_ok') is True and isinstance(v_.get('beta'), float) and isinstance(b0_, float) and abs(v_['beta'] - b0_) <= 1e-9 * abs(b0_))
    rs_ = list(h_.get('ressalvas_secao8') or []); nd_ = list(h_.get('o_que_o_teste_nao_decide') or [])
    ress_ok_ = bool(len(rs_) == 7 == len(DL_.RESSALVAS_ROTULOS_PT) and list(h_.get('rotulos_das_sete_ressalvas') or []) == list(DL_.RESSALVAS_ROTULOS_PT) and len(nd_) == len(DL_.NAO_DECIDE_RESUMO_PT) == 5 and all(str(x_).strip() for x_ in rs_ + nd_) and v_.get('n_ressalvas') == 7 and rs_ == list(v_.get('ressalvas_secao8') or []))
    em_ = v_.get('a_emenda_as_claras') or {}
    emenda_ok_ = bool(all((em_.get(k_) or {}).get('ok') is True for k_ in ('a', 'b', 'c')) and not (v_.get('c6_divergencias') or {}) and not (v_.get('c9_divergencias') or []) and (v_.get('guarda_de_finitude') or {}).get('z_finitos') is True)
    gate_ok_ = bool(v_.get('gate_verdict') == ESP.get('qg_closure_gate_verdict_v410') == selo.get('qg_closure_verdict') and v_.get('escada') == ESP['escada'][1] == ESP['escada_v410_e_v411'][0])
    obs_ok_ = bool(h_.get('observed_vector_read') is True and s_.get('observed_vector_read') is True)   # o teste FOI aberto (D169): o vetor observado foi lido, uma vez
    hd_txt_ = json.dumps({k_: h_.get(k_) for k_ in ('verdict', 'estatuto', 'scope', 'limites', 'diz', 'nao_diz', 'o_que_o_teste_nao_decide', 'ressalvas_da_gerencia', 'ressalvas_secao8')}, ensure_ascii=False)
    guarda_ok_ = bool(hd_txt_ and not GFH_.violacoes(hd_txt_) and not P18H_(hd_txt_) and not v_.get('p18_violacoes') and not v_.get('frases_violacoes') and not any(t_ in hd_txt_ for t_ in DL_.TOKENS_PROIBIDOS_V411)
                      and DL_.FRASE_H0DN_OBRIGATORIA_PT not in hd_txt_ and DL_.FRASE_H0DN_OBRIGATORIA_EN not in hd_txt_ and not re.search(r'(?i)leitura\s+do\s+operador|leitura\s+dele', hd_txt_))
    pin_ok_ = bool(len(h_.get('insumos_pinados') or {}) == len(DL_.INSUMOS_V411) and all((h_['insumos_pinados'].get(i_['nome']) or {}).get('sha256') == i_['sha256'] and (h_['insumos_pinados'].get(i_['nome']) or {}).get('bytes') == i_['bytes'] for i_ in DL_.INSUMOS_V411)
                   and len(h_.get('citados_nao_embutidos') or []) == len(DL_.CITADOS_V411) and all(any(x_.get('sha256') == c1_['sha256'] for x_ in h_['citados_nao_embutidos']) for c1_ in DL_.CITADOS_V411) and list(h_.get('contratos_de_registro_fora_da_escada') or []) == list(DL_.CONTRATOS_DE_REGISTRO_FORA_DA_ESCADA)
                   and not (v_.get('sob_pasta_vedada') or []))
    m_h_ = re.search(r'^H0DN x BG1 ABERTO \[v411[^\n]*\n  primario \(modelo publicado\): Z nulo = (\S+) ; Z K = (\S+) ; ramo (\S+)  \|\|  Cefeidas livres \(ao lado, no mesmo item\): Z nulo = (\S+) ; Z K = (\S+) ; ramo (\S+)  \|\|  checagens ok = (\d+)/(\d+) ; gate = ([^\n]*)\n  >>> (\S+) <<<$', out_n_, flags=re.M)
    std_ok_ = bool(m_h_ and m_h_.group(1) == str(p_.get('z_null')) and m_h_.group(2) == str(p_.get('z_tgl')) and m_h_.group(3) == str(p_.get('ramo')) and m_h_.group(4) == str(c_.get('z_null')) and m_h_.group(5) == str(c_.get('z_tgl')) and m_h_.group(6) == str(c_.get('ramo'))
                   and m_h_.group(7) == str(sum(1 for c1_ in chk_ if c1_.get('ok'))) and m_h_.group(8) == str(len(chk_)) and m_h_.group(9).strip() == 'o mesmo da base' and m_h_.group(10) == ver_)
    selo_ok_ = bool(s_ and set(s_) == set(H0_SELO_CHAVES) and all(_feq(s_.get(k_), h_.get(k_)) for k_ in H0_SELO_CHAVES) and s_.get('all_verified') is True and s_.get('does_not_gate_core') is True and s_.get('n_checks_esperadas') == DL_.N_CHECKS_FECHO)
    ok_ = bool(sel_ok_ and ver_ok_ and mech_ok_ and duas_ok_ and esp_ok_ and beta_ok_ and ress_ok_ and emenda_ok_ and gate_ok_ and obs_ok_ and guarda_ok_ and pin_ok_ and std_ok_ and selo_ok_)
    F = {'registro': DL_.FECHO_REGISTRO, 'verdict': h_.get('verdict'), 'ok': h_.get('all_verified'), 'sealed': ok_, 'n_checks': m_.get('n_checks'), 'mech_ok': mech_ok_, 'values_ok': esp_ok_, 'beta_ok': beta_ok_, 'runtime_executed': h_.get('runtime_executed'), 'does_not_gate_core': h_.get('does_not_gate_core'),
         'opened_once': h_.get('opened_once'), 'observed_vector_read': h_.get('observed_vector_read'), 'cabeca_do_teste': h_.get('cabeca_do_teste'), 'outcome': h_.get('outcome'), 'primario': p_, 'cefeidas_livres': c_, 'linha_ao_lado_cefeidas_livres': h_.get('linha_ao_lado_cefeidas_livres'),
         'lei_em_km_s_Mpc': v_.get('lei_em_km_s_Mpc'), 'atos': v_.get('atos'), 'ressalvas': rs_, 'rotulos_das_ressalvas': list(h_.get('rotulos_das_sete_ressalvas') or []), 'nao_decide': nd_, 'ressalvas_da_gerencia': list(h_.get('ressalvas_da_gerencia') or []),
         'n_insumos': len(h_.get('insumos_pinados') or {}), 'insumos_sha16': {k_: str((x_ or {}).get('sha256'))[:16] for k_, x_ in (h_.get('insumos_pinados') or {}).items()}, 'veredito_montado': v_.get('veredito_montado'), 'stdout_ok': std_ok_, 'selo_ok': selo_ok_, 'guarda_ok': guarda_ok_, 'ressalvas_ok': ress_ok_,
         'duas_linhas_ok': duas_ok_, 'gate_ok': gate_ok_, 'emenda_ok': emenda_ok_, 'esperado_ok': esp_ok_, 'finitude_ok': bool((v_.get('guarda_de_finitude') or {}).get('z_finitos') is True), 'pinos_ok': pin_ok_, 'escada': v_.get('escada'), 'alcance_de_p_igual_np': h_.get('alcance_de_p_igual_np')}
    if not obs_ok_:
        P.append('h0dn_bg1_v411: observed_vector_read tem de ser True no registro e no resumo do selo (o teste FOI aberto, uma vez: D169)')
    if not ok_:
        P.append('h0dn_bg1_v411 nao selou inteiro (selou e foi aberto uma vez %s; veredito == ESPERADOS == delta %s; as %s checagens c1..cN todas ok %s; as duas linhas, o primario e as Cefeidas livres, nos values e no veredito %s; os valores == ESPERADOS[registros_funcao_v411][h0dn] %s; beta == alfa x raiz de e do core %s; '
                 'as sete ressalvas e o que nao decide %s; a emenda as claras e o recalculo igual a abertura %s; o gate e a escada da v410 %s; os insumos e os citados pinados %s; o texto do registro limpo (P18, guarda das frases, nenhum token proibido, a frase velha da v410 ausente) %s; a linha do bloco no stdout %s; o resumo no selo %s): ver o registro no core'
                 % (sel_ok_, ver_ok_, DL_.N_CHECKS_FECHO, mech_ok_, duas_ok_, esp_ok_, beta_ok_, ress_ok_, emenda_ok_, gate_ok_, pin_ok_, guarda_ok_, std_ok_, selo_ok_))
    return F, P


def _ler_recriados_v410(core, base_core, ESP, P):
    """Os registros da v410 (os QUATRO com FUNCAO e os DOIS por spec) RECRIADOS no mesmo ponto do main: existem, selam, e o veredito e' o do core da v410 SELADA (base_v410) e o de ESPERADOS[vereditos_v410] (salvo a troca dita); os de funcao tem as mesmas checagens (n_checks);
    o kh_n1_cobertura_v410 traz a errata dos pisos ao lado, assinada pela gerencia c1, em nome proprio. Devolve {nome: {verdict, ok, sealed, ...}}; acrescenta em P."""
    out = {}; troca = set(ESP.get('troca_dita') or []); ev = ESP.get('vereditos_v410') or {}
    for k in REG_RECRIADOS_V410:
        r = core.get(k)
        if not (isinstance(r, dict) and 'verdict' in r):
            P.append('registro da v410 ausente do core (deveria ser RECRIADO no mesmo ponto do main): %s' % k); out[k] = {'verdict': None, 'ok': False, 'sealed': False}; continue
        b = base_core.get(k) or {}
        igual = bool(b and r.get('verdict') == b.get('verdict') and (not ev.get(k) or r.get('verdict') == ev.get(k)))
        sealed = bool(r.get('all_verified') is True and r.get('does_not_gate_core') is True and not GUARDA.search(str(r.get('verdict') or '')) and (igual or k in troca))
        if k in REG_RECRIADOS_V410F:
            sealed = bool(sealed and r.get('runtime_executed') is True and (r.get('mechanics') or {}).get('n_checks') == (b.get('mechanics') or {}).get('n_checks'))
        out[k] = {'verdict': r.get('verdict'), 'ok': r.get('all_verified'), 'sealed': sealed, 'n_checks': (r.get('mechanics') or {}).get('n_checks'), 'igual_ao_core_da_v410': igual}
        if not sealed:
            P.append('%s (registro da v410, RECRIADO): nao selou ou o veredito/as checagens diferem do core da v410 selada (base_v410) e de ESPERADOS[vereditos_v410]' % k)
    kh = core.get('kh_n1_cobertura_v410') or {}
    er = [e for e in (kh.get('erratas') or []) if 'kh_n1_cobertura_v410' in str(e.get('ao_lado_de'))]
    kb_ = base_core.get('kh_n1_cobertura_v410') or {}; ke_ = kh.get('erratas') or []; keb_ = kb_.get('erratas') or []   # a errata A MAIS da v411 (a dos pisos) mora AQUI: as da v410 selada intactas e UMA nova ao lado
    mais1_ = bool(keb_ and len(ke_) == len(keb_) + 1 and _feq(ke_[:len(keb_)], keb_) and ke_[-1] in er)
    out.setdefault('kh_n1_cobertura_v410', {})['errata_dos_pisos'] = bool(er and mais1_ and all(str(e.get('assinatura', '')).startswith('gerencia c1') and 'em nome proprio' in str(e.get('assinatura', '')) for e in er))
    if not out['kh_n1_cobertura_v410']['errata_dos_pisos']:
        P.append('kh_n1_cobertura_v410 (RECRIADO): falta a errata ao lado dos pisos (h2, h3, h6, h8), assinada pela gerencia c1, em nome proprio, UMA a mais que as da v410 selada (que seguem intactas)')
    return out


def _ler_specs_v411(core, ESP, DL_, GF_, P):
    """Os dois registros por spec NOVOS da v411: cunhagens_v411 (as ordens e ratificacoes do operador de 11 e 12/11 CITADAS por data e sha256, nao transcritas, D181; as decisoes do delta; E41 a E44 e a errata dos pisos, todas assinadas pela gerencia c1, em nome proprio; as sete ressalvas por rotulo; os textos da gerencia so' citados por sha256; D65)
    e kh_n1_cobertura_v411 (a cobertura exata do Audit: nenhum modulo novo). Devolve (V['cunhagens'], kh_ok); acrescenta em P."""
    cu = core.get(DL_.CUNHAGENS_REGISTRO) or {}; kh = core.get(DL_.KH_REGISTRO) or {}; cx_ = cu.get('extras') or {}; vb_ = cu.get('verbatim') or {}
    chaves_ = {'v411_cun_' + f_['sha256'][:16]: f_ for f_ in DL_.FALAS_V411}
    import conferir_conversa_v411 as CC_   # (R1, D181) as falas CITADAS: data, sha256 (igual ao pino da construcao), papel e autor; sem texto, sem trecho, sem nome de arquivo e sem a lista das falas fora do desenho
    ec_ = ESP.get('cunhagens') or {}   # a autoria de cada fala e' lida do proprio item citado, de extras.autores do core e dos ESPERADOS (cunhagens; chaves derivadas do sha256)
    verb_ok_ = bool(len(vb_) == len(chaves_) == DL_.N_FALAS_V411 and set(vb_) == set(chaves_) and all((vb_[k_] or {}).get('sha256') == chaves_[k_]['sha256'] for k_ in chaves_) and CC_.citadas_ok(cu, ec_, DL_.N_FALAS_V411))
    todas_op_ = bool(vb_ and ec_ and all((vb_[k_] or {}).get('autor', 'operador') == 'operador' for k_ in vb_) and set(ec_) == set(chaves_) and all((ec_[k_] or {}).get('autor') == 'operador' for k_ in ec_) and bool(cx_.get('autores')) and all(a_ == 'operador' for a_ in (cx_.get('autores') or {}).values()) and len(cx_.get('autores') or {}) == len(chaves_) and set(cx_.get('autores') or {}) == set(chaves_))
    err_ = cu.get('erratas') or []
    erratas_ok_ = bool(len(err_) == len(DL_.ERRATAS_V411) + 1 and all(e_.get('assinatura') == DL_.ASSINA for e_ in err_) and [e_.get('agora') for e_ in err_[:len(DL_.ERRATAS_V411)]] == [e_['texto'] for e_ in DL_.ERRATAS_V411]
                       and 'kh_n1_cobertura_v410' in str(err_[-1].get('ao_lado_de')) and cx_.get('assinatura_das_erratas') == DL_.ASSINA and list(cx_.get('erratas_ids') or []) == list(DL_.ERRATAS_IDS_V411))
    decisoes_ok_ = bool(dict(cx_.get('decisoes') or {}) == dict(DL_.DECISOES_V411) and all(re.fullmatch(r'D\d{3}', k_) for k_ in DL_.DECISOES_V411) and '_'.join(DL_.DECISOES_V411) == DL_.DECISOES_TOKEN_V411 and {'D159', 'D162', 'D167', 'D168', 'D169', 'D170'} <= set(DL_.DECISOES_V411) and all(str(x_).strip() for x_ in DL_.DECISOES_V411.values()))
    ressalvas_ok_ = bool(list(cx_.get('ressalvas_rotulos') or []) == list(DL_.RESSALVAS_ROTULOS_PT) and len(DL_.RESSALVAS_ROTULOS_PT) == 7)
    contagens_ok_ = bool(cx_.get('n_falas') == len(vb_) == DL_.N_FALAS_V411 and [(g_.get('nome'), g_.get('sha256')) for g_ in (cx_.get('textos_da_gerencia_citados') or [])] == [(g_['nome'], g_['sha256']) for g_ in DL_.TEXTOS_DA_GERENCIA_CITADOS]
                         and 'falas_fora_do_desenho' not in cx_)   # (D181) a lista das falas FORA do desenho saiu do programa
    alcance_ok_ = bool(str(cx_.get('alcance_de_p_igual_np') or '').startswith('P = nP ') and DL_.D10.FRASE_QUALIFICADOR_PT in str(cx_.get('alcance_de_p_igual_np')))
    sem_leitura_ok_ = bool(list(cu.get('leituras_do_operador') or []) == [] and not re.search(r'(?i)leitura\s+do\s+operador|leitura\s+dele', json.dumps({k_: cu.get(k_) for k_ in ('estatuto', 'limites', 'diz', 'nao_diz')}, ensure_ascii=False)))   # a regra do nome (D122, D123): nenhuma leitura do operador no registro novo
    fora_ok_ = bool(not any(x_.lower() in json.dumps(cu, ensure_ascii=False).lower() for x_ in DL_.FORA_D65))
    checks_cu_ok_ = bool(cu.get('checks')) and all(c_.get('ok') is True for c_ in cu.get('checks'))
    moldura_ok_ = bool(all(not GF_.violacoes(json.dumps({k_: (core.get(n_) or {}).get(k_) for k_ in ('verdict', 'estatuto', 'scope', 'limites', 'diz', 'nao_diz')}, ensure_ascii=False)) for n_ in REG_FIXOS) and (GF_.controle_negativo() or {}).get('ok') is True)
    kh_ok_ = bool(kh.get('all_verified') is True and kh.get('does_not_gate_core') is True and bool(_ev(ESP, DL_.KH_REGISTRO)) and kh.get('verdict') == _ev(ESP, DL_.KH_REGISTRO) and bool(kh.get('checks')) and all(c_.get('ok') is True for c_ in kh.get('checks')) and not GUARDA.search(str(kh.get('verdict') or '')))
    cu_ok_ = bool(verb_ok_ and todas_op_ and checks_cu_ok_ and cu.get('all_verified') is True and cu.get('does_not_gate_core') is True and erratas_ok_ and decisoes_ok_ and ressalvas_ok_ and contagens_ok_ and alcance_ok_ and sem_leitura_ok_ and fora_ok_ and moldura_ok_
                  and bool(_ev(ESP, DL_.CUNHAGENS_REGISTRO)) and cu.get('verdict') == _ev(ESP, DL_.CUNHAGENS_REGISTRO) and not GUARDA.search(str(cu.get('verdict') or '')))
    Vc = {'n': len(vb_), 'ok': cu_ok_, 'verbatim_ok': verb_ok_, 'todas_do_operador': todas_op_, 'n_trechos': 0, 'checks_ok': checks_cu_ok_, 'n_checks': len(cu.get('checks') or []), 'verdict': cu.get('verdict'), 'kernel_ok': True, 'erratas_ok': erratas_ok_, 'n_erratas': len(err_), 'decisoes_ok': decisoes_ok_,
          'n_decisoes': len(cx_.get('decisoes') or {}), 'ressalvas_ok': ressalvas_ok_, 'contagens_ok': contagens_ok_, 'alcance_ok': alcance_ok_, 'sem_leitura_ok': sem_leitura_ok_, 'moldura_ok': moldura_ok_, 'kh_ok': kh_ok_}
    if not cu_ok_:
        P.append('cunhagens_v411 nao selou como o ensaio a seco (as %d falas CITADAS por data e sha256, nao transcritas, todas do operador %s %s; as checagens %s; as erratas E41 a E44 e a dos pisos, assinadas pela gerencia c1 %s; as decisoes do delta %s; as sete ressalvas %s; as contagens e os textos da gerencia so\' citados %s; o alcance de P = nP %s; nenhuma leitura do operador %s; D65 %s; a moldura %s)'
                 % (DL_.N_FALAS_V411, verb_ok_, todas_op_, checks_cu_ok_, erratas_ok_, decisoes_ok_, ressalvas_ok_, contagens_ok_, alcance_ok_, sem_leitura_ok_, fora_ok_, moldura_ok_))
    if not kh_ok_:
        P.append('kh_n1_cobertura_v411 nao selou como o ensaio a seco (selo, veredito, checagens, nao move o gate)')
    return Vc, kh_ok_

def ler():
    P = []
    ESP = json.load(open(os.path.join(PK, 'ESPERADOS_v411.json'), encoding='utf-8')); CM = json.load(open(os.path.join(PK, 'CANDIDATO_v411.json'), encoding='utf-8'))
    ap, app = _aplicado()
    REG_TODOS = tuple(REG_FIXOS)
    core = json.load(open(os.path.join(NOS, 'um_absoluto.json'), encoding='utf-8'))['core']; selo = json.load(open(os.path.join(NOS, 'um_absoluto_selo.json'), encoding='utf-8'))
    stp = os.path.join(NOS, 'rodada_v411_stdout.txt'); out = open(stp, encoding='utf-8', errors='replace').read() if os.path.exists(stp) else ''
    V = {'nos': NOS, 'aplicado_json': app, 'pk': PK}
    if not out:
        P.append('rodada_v411_stdout.txt ausente ou vazio')
    V['s64'] = sha(os.path.join(NOS, 'um.py')); V['s16'] = V['s64'][:16]; V['umb'] = os.path.getsize(os.path.join(NOS, 'um.py'))
    if str((selo.get('sha256') or {}).get('um.py', '')) != V['s64']:
        P.append('selo.sha256(um.py) != disco')
    if not (ap['um_py_novo']['sha16'] == V['s16'] == ESP['candidato_sha16'] == CM['sha16']):
        P.append('um.py do disco != instalado/esperado/candidato')
    V['base16'] = ap['backups']['um.py']['sha16']; V['base_backup'] = ap['backups']['um.py']['backup']
    if V['base16'] != ESP['origem_sha16']:
        P.append('a base substituida != a v410 selada')
    V['n_patches'] = len(CM['patches']); V['patches'] = ', '.join(p['id'] for p in CM['patches']); V['patch_ids'] = [p['id'] for p in CM['patches']]
    V['instalado_em'] = '%s-%s-%s %s:%s:%s' % (ap['ts'][0:4], ap['ts'][4:6], ap['ts'][6:8], ap['ts'][9:11], ap['ts'][11:13], ap['ts'][13:15])
    m = re.search(r'teoremas limpos:\s*(\d+)/(\d+)', out); V['teor'] = '%s/%s' % m.groups() if m else 'AUSENTE'
    V['escada_antes'] = ESP['escada_v410_e_v411'][0]; V['escada_depois'] = ESP['escada'][1]
    if V['escada_antes'] != V['escada_depois']:
        P.append('a escada da v411 (%s) tem de ser a da v410 (%s): a v411 nao tem modulo novo' % (V['escada_depois'], V['escada_antes']))
    esc_ = core.get('external_ladder') or {}   # (a escada do CORE tambem e' lida aqui, nao so' no conferidor: o controle negativo da escada da v411 muta external_ladder e pede que a leitura recuse)
    if [esc_.get('n_theorems_clean'), esc_.get('n_theorems_expected')] != [ESP['escada'][1], ESP['escada'][1]]:
        P.append('a escada da v411 no core (external_ladder: %s de %s) tem de ser a esperada (%s de %s): a v411 nao tem modulo novo' % (esc_.get('n_theorems_clean'), esc_.get('n_theorems_expected'), ESP['escada'][1], ESP['escada'][1]))
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
    if len([l for l in out.splitlines() if '[v411]' in l]) < 1:
        P.append('o stdout nao tem a linha [v411]')
    avisos_ = [l.strip()[:200] for l in out.splitlines() if '[v411] AVISO' in l or '[v410] AVISO' in l or '[v409] AVISO' in l or '[v408] AVISO' in l or '[v407] AVISO' in l or '[v406] AVISO' in l or '[v405] AVISO' in l or '[v404] AVISO' in l or '[v403] AVISO' in l or '[v402] AVISO' in l or '[v401] AVISO' in l or '[v399] AVISO' in l or '[selo_acom] AVISO' in l]
    if avisos_:
        P.append('o stdout traz AVISO da v411 (o registro com funcao h0dn_bg1_v411, os registros por spec da v411, os registros da v410 recriados, o traducao_turing_v409, o tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 herdados e os registros recriados da v410 e anteriores, da v403, da v402, da v401 ou da v399, o selo ACOM, a declaracao do operador ou o sidecar nao rodaram): %s' % avisos_[:2])
    elif [l for l in out.splitlines() if re.search(r'\[v39[3-8]\] AVISO', l)]:
        P.append('o stdout traz AVISO de um bloco anterior (v393 a v398): %s' % [l.strip()[:200] for l in out.splitlines() if re.search(r'\[v39[3-8]\] AVISO', l)][:2])
    if [l for l in out.splitlines() if '[v403] RECUSA' in l]:
        P.append('o stdout traz a RECUSA do registro bandeiras_do_gate_v403 (uma bandeira CALCULADA do gate veio False ou uma checagem do registro falhou: fail-closed): %s' % [l.strip()[:200] for l in out.splitlines() if '[v403] RECUSA' in l][:1])
    if [l for l in out.splitlines() if '[v404] RECUSA' in l]:
        P.append('o stdout traz a RECUSA do registro f2b_errata_v404 (uma checagem da errata de F2b falhou: o canal fica como antes e o rito para; fail-closed): %s' % [l.strip()[:200] for l in out.splitlines() if '[v404] RECUSA' in l][:1])
    BC_ = _base_core(PK)   # o core da v410 SELADA (copia de bytes): de onde saem as checagens e os valores dos registros RECRIADOS

    def _rf(n_):
        r_ = BC_.get(n_) or {}
        return {'nome': n_, 'verdict': _ev(ESP, n_), 'values': r_.get('values'), 'n_checks': (r_.get('mechanics') or {}).get('n_checks')}
    RF_ = {}   # v411: nao ha' registro por pedra
    RF4_ = {k_: _rf(n_) for k_, n_ in (('projecao', 'projecao_transversal_v404'), ('jo8v32', 'jo8v32_v404'), ('f2b', 'f2b_errata_v404'))}   # projecao|jo8v32|f2b -> {nome, verdict, values, n_checks} dos registros da v404 (recriados pelo rito da v411; iguais a v410 selada)
    RF3_ = {k_: _rf(n_) for k_, n_ in (('caminho', 'caminho_v403'), ('vida', 'vida_v403'), ('verdade_adendo', 'verdade_adendo_v403'), ('gate', 'bandeiras_do_gate_v403'))}   # o mesmo, dos registros da v403 (recriados)
    EV2_ = ESP.get('vereditos_v410') or {}   # os vereditos da v410 SELADA (os registros anteriores sao recriados e tem de dar os mesmos)
    R410SPEC_ = {k_: _ev(ESP, k_) for k_ in REG_V410C[8:]}; R411SPEC_ = {k_: _ev(ESP, k_) for k_ in REG_SPEC_V411}; R410TSPEC_ = {k_: _ev(ESP, k_) for k_ in REG_V410T[1:]}; R408DSPEC_ = {k_: _ev(ESP, k_) for k_ in REG_V408D[1:]}; R407DSPEC_ = {k_: _ev(ESP, k_) for k_ in REG_V407D[1:]}; R406DSPEC_ = {k_: _ev(ESP, k_) for k_ in REG_V406D[1:]}   # os registros por spec da v405 (recriados), da v411 (novos), da v410, da v407 e da v406 (herdados)
    for r_, e_ in (('selo_pela_propria_tecnologia_v399', (ESP.get('selo_acom') or {}).get('verdict')), ('declaracao_do_operador_v399', (ESP.get('declaracao') or {}).get('verdict')), ('falsidade_da_inercia_v401', ESP.get('veredito_da_falsidade_v410')),
                   ('ponte_da_escala_dual_v402', EV2_.get('ponte_da_escala_dual_v402')), ('queda_sem_geometria_v402', EV2_.get('queda_sem_geometria_v402')), ('esperanca_condicional_v402', EV2_.get('esperanca_condicional_v402')),
                   ('caminho_v403', (RF3_.get('caminho') or {}).get('verdict')), ('vida_v403', (RF3_.get('vida') or {}).get('verdict')), ('verdade_adendo_v403', (RF3_.get('verdade_adendo') or {}).get('verdict')), ('bandeiras_do_gate_v403', (RF3_.get('gate') or {}).get('verdict')),
                   ('projecao_transversal_v404', (RF4_.get('projecao') or {}).get('verdict')), ('jo8v32_v404', (RF4_.get('jo8v32') or {}).get('verdict')), ('f2b_errata_v404', (RF4_.get('f2b') or {}).get('verdict'))) + tuple((n_, _ev(ESP, n_)) for n_ in REG_V410C[:8]) + (('fechamento_v406', _ev(ESP, 'fechamento_v406')), ('psion_canto_v407', _ev(ESP, 'psion_canto_v407')), ('tetelestai_terminal_v408', _ev(ESP, 'tetelestai_terminal_v408')), ('traducao_turing_v409', _ev(ESP, 'traducao_turing_v409')), ('iald2_v410', _ev(ESP, 'iald2_v410')), ('a_escala_v410', _ev(ESP, 'a_escala_v410')), ('h0dn_bg1_v410', _ev(ESP, 'h0dn_bg1_v410')), ('h0dn_fontes_hms13_v410', _ev(ESP, 'h0dn_fontes_hms13_v410')), ('h0dn_bg1_v411', _ev(ESP, 'h0dn_bg1_v411'))):   # (09/11, parte 2: os QUATRO registros com funcao da v411 tem a linha `>>> veredito <<<` do ensaio a seco no stdout)
        if not e_ or ('>>> %s <<<' % e_) not in out:
            P.append('o bloco %s do stdout nao traz a linha `>>> veredito <<<` do ensaio a seco' % r_)
    m_s9 = re.search(r'\[v399\] o selo pela propria tecnologia e a declaracao do operador \(lidos depois da afinacao das cordas\) e as inscricoes de 24/10 \(cunhagens_v399\): selo=(\S+) \| declaracao=(\S+) \| cunhagens=(\S+) \| registros por spec: (\d+) \(selados (\d+)\)', out)
    if (not m_s9 or (m_s9.group(1), m_s9.group(2), m_s9.group(3)) != ((ESP.get('selo_acom') or {}).get('verdict'), (ESP.get('declaracao') or {}).get('verdict'), (ESP.get('registros_v399') or {}).get('cunhagens_v399'))
            or m_s9.group(4) != m_s9.group(5) or int(m_s9.group(4)) != len(ESP.get('registros_v399') or {})):
        P.append('a linha [v399] do stdout (selo, declaracao e cunhagens_v399; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(ESP.get('registros_v399') or {}), m_s9.groups()[3:] if m_s9 else 'ausente'))
    m_s1 = re.search(r'\[v401\] a falsidade \(simulacro\) da inercia \(lida depois da declaracao do operador\) e as inscricoes de 25/10 \(cunhagens_v401\): falsidade=(\S+) \| cunhagens=(\S+) \| registros por spec: (\d+) \(selados (\d+)\)', out)
    if (not m_s1 or (m_s1.group(1), m_s1.group(2)) != (ESP.get('veredito_da_falsidade_v410'), (ESP.get('registros_v401') or {}).get('cunhagens_v401')) or m_s1.group(3) != m_s1.group(4) or int(m_s1.group(3)) != len(ESP.get('registros_v401') or {})):
        P.append('a linha [v401] do stdout (falsidade e cunhagens_v401, recriados; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(ESP.get('registros_v401') or {}), m_s1.groups()[2:] if m_s1 else 'ausente'))
    m_s2 = re.search(r'\[v402\] a ponte, a queda e a esperanca \(lidas depois da falsidade da inercia\) e as inscricoes de 26/10 \(cunhagens_v402\): ponte=(\S+) \| queda=(\S+) \| esperanca=(\S+) \| cunhagens=(\S+) \| registros por spec: (\d+) \(selados (\d+)\)', out)
    if (not m_s2 or (m_s2.group(1), m_s2.group(2), m_s2.group(3), m_s2.group(4)) != (EV2_.get('ponte_da_escala_dual_v402'), EV2_.get('queda_sem_geometria_v402'), EV2_.get('esperanca_condicional_v402'), (ESP.get('registros_v402') or {}).get('cunhagens_v402'))
            or m_s2.group(5) != m_s2.group(6) or int(m_s2.group(5)) != len(ESP.get('registros_v402') or {})):
        P.append('a linha [v402] do stdout (ponte, queda, esperanca e cunhagens_v402, recriados; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(ESP.get('registros_v402') or {}), m_s2.groups()[4:] if m_s2 else 'ausente'))
    m_s3 = re.search(r'\[v403\] o caminho, a vida, o adendo da verdade e as bandeiras do gate \(lidos depois da esperanca condicional\) e as falas de 27/10 \(cunhagens_v403\): caminho=(\S+) \| vida=(\S+) \| verdade_adendo=(\S+) \| bandeiras=(\S+) \| cunhagens=(\S+) \| registros por spec: (\d+) \(selados (\d+)\)', out)
    if (not m_s3 or tuple(m_s3.group(i_) for i_ in range(1, 6)) != ((RF3_.get('caminho') or {}).get('verdict'), (RF3_.get('vida') or {}).get('verdict'), (RF3_.get('verdade_adendo') or {}).get('verdict'), (RF3_.get('gate') or {}).get('verdict'), (ESP.get('registros_v403') or {}).get('cunhagens_v403'))
            or m_s3.group(6) != m_s3.group(7) or int(m_s3.group(6)) != len(ESP.get('registros_v403') or {})):
        P.append('a linha [v403] do stdout (caminho, vida, verdade_adendo, bandeiras e cunhagens_v403, recriados; registros por spec selados == %d) esta ausente ou difere da v410 selada (%s)' % (len(ESP.get('registros_v403') or {}), m_s3.groups()[5:] if m_s3 else 'ausente'))
    m_s4 = re.search(r'\[v404\] a projecao transversal, o jo8v32 e a errata de F2b \(a projecao e o jo8v32 lidos depois das bandeiras do gate; a errata de F2b depois da errata ao lado de R6 da v386\) e as falas de 28/10 \(cunhagens_v404\): projecao=(\S+) \| jo8v32=(\S+) \| f2b=(\S+) \| cunhagens=(\S+) \| registros por spec: (\d+) \(selados (\d+)\)', out)
    if (not m_s4 or tuple(m_s4.group(i_) for i_ in range(1, 5)) != ((RF4_.get('projecao') or {}).get('verdict'), (RF4_.get('jo8v32') or {}).get('verdict'), (RF4_.get('f2b') or {}).get('verdict'), (ESP.get('registros_v404') or {}).get('cunhagens_v404'))
            or m_s4.group(5) != m_s4.group(6) or int(m_s4.group(5)) != len(ESP.get('registros_v404') or {})):
        P.append('a linha [v404] do stdout (projecao, jo8v32, f2b e cunhagens_v404; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(ESP.get('registros_v404') or {}), m_s4.groups()[4:] if m_s4 else 'ausente'))
    m_s5 = re.search(r'\[v405\] os oito registros com funcao \(lidos depois dos tres da v404\) e os registros por spec da v405: (.*?) \| specs: (\d+) \(selados (\d+)\)', out)
    if not m_s5 or len(m_s5.group(1).split(' | ')) != 8 or {x_.split('=')[-1] for x_ in m_s5.group(1).split(' | ')} != {'SELOU'} or m_s5.group(2) != m_s5.group(3) or int(m_s5.group(2)) != 5:
        P.append('a linha [v405] do stdout (os oito registros com funcao SELOU; registros por spec selados == 5) esta ausente ou difere do ensaio a seco (%s)' % repr(m_s5.groups()[1:] if m_s5 else 'ausente'))
    m_s6 = re.search(r'\[v406\] o fechamento e os registros por spec da v406: fechamento=(\S+) \| specs: (\d+) \(selados (\d+)\)', out)   # a linha HERDADA da v406: o main da v411 segue rodando o bloco do fechamento_v406; o texto e' o que o um.py imprime («da v406»)
    if not m_s6 or m_s6.group(1) != 'SELOU' or m_s6.group(2) != m_s6.group(3) or int(m_s6.group(2)) != len(REG_V406D) - 1:
        P.append('a linha [v406] do stdout (fechamento_v406 SELOU; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(REG_V406D) - 1, repr(m_s6.groups() if m_s6 else 'ausente')))
    m_s7 = re.search(r'\[v407\] o registro do psion e do canto e os registros por spec da v407: psion_canto=(\S+) \| specs: (\d+) \(selados (\d+)\)', out)   # a linha HERDADA da v407: o main da v411 segue rodando o bloco do psion e do canto; o texto e' o que o um.py imprime («da v407»)
    if not m_s7 or m_s7.group(1) != 'SELOU' or m_s7.group(2) != m_s7.group(3) or int(m_s7.group(2)) != len(REG_V407D) - 1:
        P.append('a linha [v407] do stdout (psion_canto SELOU; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(REG_V407D) - 1, repr(m_s7.groups() if m_s7 else 'ausente')))
    m_s8t = re.search(r'\[v408\] o registro do terminal e os registros por spec da v408: tetelestai_terminal=(\S+) \| specs: (\d+) \(selados (\d+)\)', out)   # a linha HERDADA da v408 (o texto e' o que o um.py imprime: «da v408»)
    if not m_s8t or m_s8t.group(1) != 'SELOU' or m_s8t.group(2) != m_s8t.group(3) or int(m_s8t.group(2)) != len(REG_V408D) - 1:
        P.append('a linha [v408] do stdout (tetelestai_terminal SELOU; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(REG_V408D) - 1, repr(m_s8t.groups() if m_s8t else 'ausente')))
    m_s9t = re.search(r'\[v409\] o registro da traducao e os registros por spec da v409: traducao_turing=(\S+) \| specs: (\d+) \(selados (\d+)\)', out)   # a linha HERDADA da v409 (o texto e' o que o um.py imprime: «da v409»)
    if not m_s9t or m_s9t.group(1) != 'SELOU' or m_s9t.group(2) != m_s9t.group(3) or int(m_s9t.group(2)) != len(REG_V410T) - 1:
        P.append('a linha [v409] do stdout (traducao_turing SELOU; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(REG_V410T) - 1, repr(m_s9t.groups() if m_s9t else 'ausente')))
    m_s10 = re.search(r'\[v410\] os registros com funcao e os por spec da v410: ' + r' \| '.join(r'%s=(\S+)' % re.escape(n_) for n_ in REG_RECRIADOS_V410F) + r' \| specs: (\d+) \(selados (\d+)\)', out)   # a linha da v410, RECRIADA pelo rito da v411 (o texto e' o que o um.py da v410 imprime: «da v410»)
    nrf_ = len(REG_RECRIADOS_V410F)
    if not m_s10 or any(m_s10.group(i_) != 'SELOU' for i_ in range(1, nrf_ + 1)) or m_s10.group(nrf_ + 1) != m_s10.group(nrf_ + 2) or int(m_s10.group(nrf_ + 1)) != len(REG_RECRIADOS_V410S):
        P.append('a linha [v410] do stdout (os %d registros com funcao da v410 SELOU: %s; registros por spec selados == %d) esta ausente ou difere do que a v410 selou (%s)' % (nrf_, ', '.join(REG_RECRIADOS_V410F), len(REG_RECRIADOS_V410S), repr(m_s10.groups() if m_s10 else 'ausente')))
    m_s11 = re.search(r'\[v411\] o registro com funcao e os por spec da v411: ' + r' \| '.join(r'%s=(\S+)' % re.escape(n_) for n_ in REG_FUNCAO) + r' \| specs: (\d+) \(selados (\d+)\)', out)   # a linha NOVA da v411 (gerar_candidato_v411.py: N00_main_h0dn_v411)
    nrf1_ = len(REG_FUNCAO)
    if not m_s11 or any(m_s11.group(i_) != 'SELOU' for i_ in range(1, nrf1_ + 1)) or m_s11.group(nrf1_ + 1) != m_s11.group(nrf1_ + 2) or int(m_s11.group(nrf1_ + 1)) != len(REG_SPEC_V411):
        P.append('a linha [v411] do stdout (o registro com funcao %s SELOU; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (', '.join(REG_FUNCAO), len(REG_SPEC_V411), repr(m_s11.groups() if m_s11 else 'ausente')))
    # a linha [v398] que o main da v411 segue imprimindo (o sonico, a afinacao das cordas e as cunhagens da v398): igual ao que a v410 selou
    ev8_ = ESP.get('vereditos_v410') or {}
    n_spec8_ = len([k_ for k_ in REG_V398 if k_ not in ('sonico_v398', 'afinacao_das_cordas_v398')])
    m_s8 = re.search(r'\[v398\] o sonico e a afinacao das cordas \(lidos na fractalizacao do Um\) e as inscricoes de 23/10 \(cunhagens_v398\): sonico=(\S+) \| afinacao=(\S+) \| cunhagens=(\S+) \| registros por spec: (\d+) \(selados (\d+)\)', out)
    if (not m_s8 or (m_s8.group(1), m_s8.group(2), m_s8.group(3)) != (ev8_.get('sonico_v398'), ev8_.get('afinacao_das_cordas_v398'), ev8_.get('cunhagens_v398')) or m_s8.group(4) != m_s8.group(5) or int(m_s8.group(4)) != n_spec8_):
        P.append('a linha [v398] do stdout (sonico, afinacao e cunhagens_v398; registros por spec selados == %d) esta ausente ou difere da que a v410 selou (%s)' % (n_spec8_, m_s8.groups()[3:] if m_s8 else 'ausente'))
    # as duas linhas [v397] que o main da v411 segue imprimindo (o Teste da Unica Palavra e as cunhagens da v397): iguais ao que a v397 selou
    m_tv = re.search(r'\[v397\] o Teste da Unica Palavra \(Fase 9 V2-c1, aberto uma vez em 23/10\), lido por hash ao lado do V1 \(nenhum sigma novo\): (\S+)', out)
    if not m_tv or m_tv.group(1) != ev8_.get('teste_de_veracidade_fase9_v397'):
        P.append('a linha [v397] do Teste da Unica Palavra esta ausente do stdout ou difere da que a v397 selou (%s)' % (m_tv.group(1)[:80] if m_tv else 'ausente'))
    n_spec7_ = len([k_ for k_ in REG_V397 if k_ != 'teste_de_veracidade_fase9_v397'])
    m_sp = re.search(r'\[v397\] a pedra Token e as falas de 23/10 \(cunhagens_v397\): (\S+) \| registros por spec: (\d+) \(selados (\d+)\)', out)
    if not m_sp or m_sp.group(1) != ev8_.get('cunhagens_v397') or m_sp.group(2) != m_sp.group(3) or int(m_sp.group(2)) != n_spec7_:
        P.append('a linha [v397] das cunhagens da v397 esta ausente do stdout ou difere da que a v397 selou (registros por spec selados == %d)' % n_spec7_)
    hp = os.path.join(PK, 'rito_horarios_v411.txt'); V['horarios'] = open(hp, encoding='utf-8').read().split() if os.path.exists(hp) else []
    V['selo_ts'] = selo.get('timestamp'); V['um_version'] = selo.get('um_version'); V['qg'] = selo.get('qg_closure_verdict')
    if V['um_version'] != 'v411':
        P.append('o selo nao e v411')
    if V['qg'] != ESP['qg_closure_verdict']:
        P.append('o gate MUDOU')
    qg = core.get('qg_closure') or {}
    V['n18'] = sum(1 for fam in ('formal_flags', 'physics_flags', 'experiment_flags') for v in (qg.get(fam) or {}).values() if v is True)
    if V['n18'] != 18:
        P.append('as bandeiras do gate nao sao 18 True (%s)' % V['n18'])
    for k in ('um_absoluto.json', 'um_absoluto_selo.json', 'um_absoluto_selo_acom.json', 'um_absoluto_forma_canonica.md', 'um_absoluto_manifest.md'):
        V['h_' + k] = sha(os.path.join(NOS, k))[:16] if os.path.exists(os.path.join(NOS, k)) else 'AUSENTE'
    V['artigos'] = {os.path.basename(p): sha(p)[:16] for p in sorted(glob.glob(os.path.join(NOS, 'um_absoluto_??.pdf')) + glob.glob(os.path.join(NOS, 'um_absoluto_??.txt')))}
    cp = os.path.join(HERE, 'conferidor', 'conferencia_rito_v411.json')
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
        if C.get('veredito_falsidade') != ESP.get('veredito_da_falsidade_v410'):
            P.append('a conferencia do rito traz o veredito da falsidade (falsidade_da_inercia_v401) diferente do ensaio a seco')
        for chv_, esp_v_, nome_ in (('veredito_ponte', EV2_.get('ponte_da_escala_dual_v402'), 'ponte_da_escala_dual_v402'), ('veredito_queda', EV2_.get('queda_sem_geometria_v402'), 'queda_sem_geometria_v402'), ('veredito_esperanca', EV2_.get('esperanca_condicional_v402'), 'esperanca_condicional_v402'),
                                    ('veredito_caminho', (RF3_.get('caminho') or {}).get('verdict'), 'caminho_v403'), ('veredito_vida', (RF3_.get('vida') or {}).get('verdict'), 'vida_v403'), ('veredito_verdade_adendo', (RF3_.get('verdade_adendo') or {}).get('verdict'), 'verdade_adendo_v403'),
                                    ('veredito_bandeiras_do_gate', (RF3_.get('gate') or {}).get('verdict'), 'bandeiras_do_gate_v403'),
                                    ('veredito_projecao', (RF4_.get('projecao') or {}).get('verdict'), 'projecao_transversal_v404'), ('veredito_jo8v32', (RF4_.get('jo8v32') or {}).get('verdict'), 'jo8v32_v404'), ('veredito_f2b', (RF4_.get('f2b') or {}).get('verdict'), 'f2b_errata_v404'),
                                    ('veredito_traducao_turing_herdado', _ev(ESP, 'traducao_turing_v409'), 'traducao_turing_v409'), ('veredito_tetelestai_terminal', _ev(ESP, 'tetelestai_terminal_v408'), 'tetelestai_terminal_v408'), ('veredito_psion_herdado', _ev(ESP, 'psion_canto_v407'), 'psion_canto_v407'), ('veredito_fechamento_herdado', _ev(ESP, 'fechamento_v406'), 'fechamento_v406')):
            if not C.get(chv_) or C.get(chv_) != esp_v_:
                P.append('a conferencia do rito traz o veredito de %s (%s) ausente ou diferente do ensaio a seco' % (nome_, chv_))
        for chv_, nomes_ in (('veredito_iald2', ('iald2_v410',)), ('veredito_h0dn', ('h0dn_bg1_v410', 'h0dn_bg1_v411')), ('veredito_h0dn_bg1_v411', ('h0dn_bg1_v411',)), ('veredito_h0dn_v411', ('h0dn_bg1_v411',)), ('veredito_a_escala', ('a_escala_v410',)), ('veredito_hms13', ('h0dn_fontes_hms13_v410',)), ('veredito_h0dn_fontes_hms13', ('h0dn_fontes_hms13_v410',))):
            if chv_ in C and C.get(chv_) not in {_ev(ESP, n_) for n_ in nomes_}:   # (o conferir_rito_v411.py pode nao emitir estas chaves; se emitir, tem de ser a do ensaio a seco de um dos registros que a chave nomeia)
                P.append('a conferencia do rito traz o veredito de %s (%s) diferente do ensaio a seco' % (' ou '.join(nomes_), chv_))
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
    V['n_ver'] = len(ESP['vereditos_v410'])
    # --- os registros novos: descobertos por comparacao com o que a v410 ja tinha
    novos = []
    for k, r in core.items():
        if isinstance(r, dict) and 'verdict' in r and k not in ESP['vereditos_v410']:
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
        P.append('a v411 cria exatamente as chaves %s com veredito no core e o core traz %s' % (sorted(REG_FIXOS), sorted(novos)))
    V['reg410_recriados'] = _ler_recriados_v410(core, _base_core(PK), ESP, P)   # os QUATRO com funcao e os DOIS por spec da v410, RECRIADOS no mesmo ponto: existem, selam, mesmo veredito da v410 selada (nao sao novos)
    V['reg410b'] = {}
    for k in REG_V410B:    # os CINCO registros da v410 SELADA sao RECRIADOS pelo rito: seguem no core, selados e iguais ao selado
        r = core.get(k)
        if not (isinstance(r, dict) and 'verdict' in r):
            P.append('registro obrigatorio ausente do core: %s' % k)
            continue
        V['reg410b'][k] = {'verdict': r.get('verdict'), 'ok': r.get('all_verified')}
        if r.get('all_verified') is not True:
            P.append('%s nao selou' % k)
        if GUARDA.search(str(r.get('verdict') or '')):
            P.append('%s com palavra proibida' % k)
        if k in (ESP.get('vereditos_v410') or {}) and k not in (ESP.get('troca_dita') or []) and r.get('verdict') != ESP['vereditos_v410'][k]:
            P.append('%s: o veredito do rito difere do ensaio a seco (a v410 selada)' % k)
    V['reg410c'] = {}
    for k in REG_V410C:    # os TREZE registros da v410 SELADA sao RECRIADOS pelo rito: seguem no core, selados e iguais a v410 selada (veredito; as checagens e os valores das oito funcoes sao conferidos adiante, em fun410c)
        r = core.get(k)
        if not (isinstance(r, dict) and 'verdict' in r):
            P.append('registro obrigatorio ausente do core: %s' % k)
            continue
        V['reg410c'][k] = {'verdict': r.get('verdict'), 'ok': r.get('all_verified')}
        if r.get('all_verified') is not True:
            P.append('%s nao selou' % k)
        if GUARDA.search(str(r.get('verdict') or '')):
            P.append('%s com palavra proibida' % k)
        if not _ev(ESP, k) or r.get('verdict') != _ev(ESP, k):
            P.append('%s: o veredito do rito difere do que a v410 selou (ESPERADOS[vereditos_v410], ou o do ensaio a seco se na troca dita)' % k)
        b_ = _base_core(PK).get(k) or {}
        # (cunhagens_v405: falas e erratas IGUAIS as da v410 selada; gap_v405 e kh_n1_cobertura_v405 ganham, na v411, uma errata ao lado (E17 / os pisos), em nome proprio da gerencia c1: as falas seguem iguais e toda errata e' assinada)
        erratas_ok_ = (_feq(r.get('erratas'), b_.get('erratas')) if k == 'cunhagens_v405' else bool(r.get('erratas') and len(r.get('erratas')) >= len(b_.get('erratas') or []) and all(str(e_.get('assinatura', '')).startswith('gerencia c1, em nome proprio') for e_ in r.get('erratas'))))
        if k in REG_V410C[8:] and not (b_ and r.get('does_not_gate_core') is True and _feq(r.get('verbatim'), b_.get('verbatim')) and erratas_ok_):
            P.append('%s (por spec, recriado): as falas embutidas, as erratas ou o gate diferem da v410 selada' % k)
    V['cunh410c'] = {'ok': bool((V['reg410c'].get('cunhagens_v405') or {}).get('ok') is True), 'verdict': (V['reg410c'].get('cunhagens_v405') or {}).get('verdict'), 'n': len((core.get('cunhagens_v405') or {}).get('verbatim') or {}), 'n_erratas': len((core.get('cunhagens_v405') or {}).get('erratas') or [])}
    V['reg410t'] = {}
    for k in REG_V410T:    # os TRES registros da v410 (HERDADOS: a traducao e os dois por spec) sao RECRIADOS pelo rito: seguem no core, selados e de veredito igual ao esperado (o da v410 selada, ou o do ensaio a seco se na troca dita: a traducao carrega a escada); o conteudo e' conferido adiante
        r = core.get(k)
        if not (isinstance(r, dict) and 'verdict' in r):
            P.append('registro obrigatorio ausente do core: %s' % k)
            continue
        V['reg410t'][k] = {'verdict': r.get('verdict'), 'ok': r.get('all_verified')}
        if r.get('all_verified') is not True:
            P.append('%s nao selou' % k)
        if GUARDA.search(str(r.get('verdict') or '')):
            P.append('%s com palavra proibida' % k)
        if not _ev(ESP, k) or r.get('verdict') != _ev(ESP, k):
            P.append('%s: o veredito do rito difere do esperado (ESPERADOS[vereditos_v410], ou o do ensaio a seco se na troca dita)' % k)
    V['reg408d'] = {}
    for k in REG_V408D:    # os TRES registros da v408 (HERDADOS) sao RECRIADOS pelo rito: seguem no core, selados e de veredito igual ao esperado (o da v410 selada, ou o do ensaio a seco se na troca dita: o terminal carrega a escada); o conteudo (checagens, erratas) e' conferido adiante
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
            P.append('%s: o veredito do rito difere do esperado (ESPERADOS[vereditos_v410], ou o do ensaio a seco se na troca dita)' % k)
    V['reg407d'] = {}
    for k in REG_V407D:    # os TRES registros da v407 (HERDADOS) sao RECRIADOS pelo rito: seguem no core, selados e de veredito igual ao esperado (o da v410 selada, ou o do ensaio a seco se na troca dita: o psion carrega a escada); o conteudo (checagens, erratas) e' conferido adiante
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
            P.append('%s: o veredito do rito difere do esperado (ESPERADOS[vereditos_v410], ou o do ensaio a seco se na troca dita)' % k)
    V['reg406d'] = {}
    for k in REG_V406D:    # os TRES registros da v406 (HERDADOS) sao RECRIADOS pelo rito: seguem no core, selados e de veredito igual ao esperado (o da v410 selada, ou o do ensaio a seco se na troca dita); o conteudo (checagens, erratas) e' conferido adiante
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
            P.append('%s: o veredito do rito difere do esperado (ESPERADOS[vereditos_v410], ou o do ensaio a seco se na troca dita)' % k)
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
        e401_ = ESP.get('veredito_da_falsidade_v410') if k == 'falsidade_da_inercia_v401' else (ESP.get('registros_v401') or {}).get(k)
        if not e401_ or r.get('verdict') != e401_:
            P.append('%s: o veredito do rito difere do ensaio a seco' % k)
    V['reg402'] = list(REG_V402); V['reg402_estado'] = {}
    for k in REG_V402:    # os CINCO registros da v402 sao RECRIADOS pelo rito: tem de seguir no core, selados e (por veredito) iguais ao que a v410 selou (ESPERADOS[vereditos_v410])
        r = core.get(k)
        if not (isinstance(r, dict) and 'verdict' in r):
            P.append('registro obrigatorio ausente do core: %s' % k)
            continue
        V['reg402_estado'][k] = {'verdict': r.get('verdict'), 'ok': r.get('all_verified')}
        if r.get('all_verified') is not True:
            P.append('%s nao selou' % k)
        if GUARDA.search(str(r.get('verdict') or '')):
            P.append('%s com palavra proibida' % k)
        e402_ = (ESP.get('vereditos_v410') or {}).get(k)
        if not e402_ or r.get('verdict') != e402_:
            P.append('%s: o veredito do rito difere do ensaio a seco' % k)
    V['reg410'] = list(REG_V410); V['reg410_estado'] = {}
    for k in REG_V410:    # os SEIS registros da v410 sao RECRIADOS pelo rito: tem de seguir no core, selados e (por veredito) iguais ao que a v410 selou (ESPERADOS[vereditos_v410])
        r = core.get(k)
        if not (isinstance(r, dict) and 'verdict' in r):
            P.append('registro obrigatorio ausente do core: %s' % k)
            continue
        V['reg410_estado'][k] = {'verdict': r.get('verdict'), 'ok': r.get('all_verified')}
        if r.get('all_verified') is not True:
            P.append('%s nao selou' % k)
        if GUARDA.search(str(r.get('verdict') or '')):
            P.append('%s com palavra proibida' % k)
        e410_ = (ESP.get('vereditos_v410') or {}).get(k)
        if not e410_ or r.get('verdict') != e410_:
            P.append('%s: o veredito do rito difere do ensaio a seco' % k)
    for k in V['troca_dita']:
        r = core.get(k) or {}
        if r.get('all_verified') is False:
            P.append('%s (troca dita) nao selou' % k)
    # v411: NENHUM modulo novo de kernel (o kernel e' o da v410, byte a byte): FLAGS_v411.json sem bandeira, CANDIDATO_v411.json sem modulo novo, ESPERADOS sem bundle; os bundles da v410, v409, v408, v407 e v406 SEGUEM no kernel do Nos e no hash formal do rito com o sha256 PINADO
    # no delta de cada versao (lido do delta, independente das chaves de ESPERADOS)
    if PK not in sys.path:
        sys.path.insert(0, PK)
    import delta_v411 as DL_   # REGISTROS_FUNCAO, REGISTROS_FUNCAO_V410, FECHO_REGISTRO, N_CHECKS_FECHO, ERRATAS_V411, DECISOES_V411, FALAS_V411, INSUMOS_V411, CITADOS_V411, D10..D6: lidos do delta, nunca digitados aqui
    FJ_ = json.load(open(os.path.join(PK, 'kernel', 'FLAGS_v411.json'), encoding='utf-8'))
    V['pedras'] = []; V['n_pedras'] = 0
    njp_ = os.path.join(PK, 'kernel_modulos_novos_v411.json'); nj_ = json.load(open(njp_, encoding='utf-8')) if os.path.exists(njp_) else {}
    kk_ = CM.get('kernel') or {}
    if not (FJ_.get('n_flags') == 0 and not (FJ_.get('flags') or []) and CM.get('n_bandeiras') == 0 and kk_.get('modulos_novos') == 0 and not (nj_.get('novos') or []) and not (ESP.get('bundle_sha256') or {}) and ((ESP.get('kernel') or {}).get('modulos_novos', 0) == 0)):
        P.append('a v411 NAO tem modulo novo de kernel: FLAGS_v411.json (n_flags=%s), CANDIDATO_v411.json (modulos_novos=%s, n_bandeiras=%s), kernel_modulos_novos_v411.json (%s novos) e ESPERADOS (bundle_sha256 vazio, kernel.modulos_novos 0) tem de dizer ZERO' % (FJ_.get('n_flags'), kk_.get('modulos_novos'), CM.get('n_bandeiras'), len(nj_.get('novos') or [])))
    if tuple(REG_FIXOS) != tuple(DL_.REGISTROS_FUNCAO) + (DL_.CUNHAGENS_REGISTRO, DL_.KH_REGISTRO) or list(DL_.REGISTROS_FUNCAO) != [DL_.FECHO_REGISTRO] or tuple(REG_RECRIADOS_V410F) != tuple(DL_.REGISTROS_FUNCAO_V410) or DL_.FECHO_REGISTRO != 'h0dn_bg1_v411':
        P.append('os nomes dos registros em leitura_v411.py != delta_v411.py (REGISTROS_FUNCAO = [h0dn_bg1_v411]; REGISTROS_FUNCAO_V410 = os quatro com funcao da v410)')
    kfs6_ = ((core.get('kernel_formalization') or {}).get('formal_files_sha256')) or {}
    for bk_, dm_, bdesc_ in (('bundle410', DL_.D10, 'v410 (%d modulos de TGLExt/: IALD2 e AEscala)'), ('bundle409', DL_.D9, 'v409 (%d modulos de TGLExt/)'), ('bundle408', DL_.D8, 'v408 (%d modulos de TGLExt/)'), ('bundle407', DL_.D7, 'v407 (%d modulos de TGLExt/)'), ('bundle406', DL_.D6, 'v406 (%d modulos de TGLExt/F1Fecho394)')):
        pins_ = {r6_: dm_.BUNDLE_POR_REL[r6_]['sha256'] for r6_ in dm_.BUNDLE_RELS}
        V[bk_] = {'n': len(pins_), 'n_ok': sum(1 for r6_, s6_ in pins_.items() if os.path.isfile(os.path.join(NOS, 'tgl_kernel', *r6_.split('/'))) and sha(os.path.join(NOS, 'tgl_kernel', *r6_.split('/'))) == s6_ and kfs6_.get(r6_) == s6_)}
        V[bk_]['ok'] = bool(pins_ and V[bk_]['n'] == V[bk_]['n_ok'] == dm_.N_BUNDLE)
        if not V[bk_]['ok']:
            P.append(('o bundle da ' + bdesc_ + ' deixou de estar no kernel do Nos / no hash formal do rito com o sha256 pinado no delta (%s ok): a v411 nao reescreve as versoes anteriores') % (dm_.N_BUNDLE, V[bk_]['n_ok']))
    vs = core.get('varredura_e_sorry_v392') or {}
    V['varr'] = vs.get('varredura') or {}; V['varr_verdict'] = vs.get('verdict')
    V['axiom_report_n'] = len((core.get('kernel_formalization') or {}).get('axiom_report') or {})
    ep = core.get('estatuto_da_prova_v391') or {}
    V['ep_verdict'] = ep.get('verdict')
    V['fd390'] = (core.get('fundacao_v390') or {}).get('verdict')
    V['verbatins'] = {f_['sha256'][:16]: {'sha16': f_['sha256'][:16], 'bytes': f_['bytes']} for f_ in DL_.FALAS_V411}
    if CM.get('falas_citadas') != DL_.N_FALAS_V411 or len(V['verbatins']) != DL_.N_FALAS_V411 or 'verbatins_embutidos' in CM:
        P.append('o CANDIDATO_v411.json nao traz as %d falas CITADAS (falas_citadas=%s) ou ainda traz verbatins_embutidos (D181: nenhuma fala embutida)' % (DL_.N_FALAS_V411, CM.get('falas_citadas')))
    # --- v411: os QUATRO registros novos (dois com FUNCAO, dois por spec) conferidos contra o ensaio a seco registrado em ESPERADOS; os da v398, da v397, da v396, da v395, da v394 e da v393 seguem no core e tem de seguir selados (os da v410, da v402, da v401 e da v399 sao recriados e conferidos acima); o sidecar; nenhum numero e' digitado
    V['reg_todos'] = list(REG_TODOS)
    for k_ in REG_V393 + REG_V394 + REG_V395 + REG_V396 + REG_V397 + REG_V398:
        if (core.get(k_) or {}).get('all_verified') is not True:
            P.append('%s (registro da v398, da v397, da v396, da v395, da v394 ou da v393) deixou de selar' % k_)
    RV_ = dict(ESP.get('vereditos_novos_v411') or {})   # registro -> veredito do ensaio a seco (projecao_transversal, jo8v32 e f2b_errata sao runtime; cunhagens_v404 e kh_n1_cobertura_v404 sao por spec)
    V['reg411'] = {}
    for k_ in REG_FIXOS:
        r_ = core.get(k_) or {}
        V['reg411'][k_] = {'verdict': r_.get('verdict'), 'ok': r_.get('all_verified')}
        esp_v_ = RV_.get(k_)
        if esp_v_ is None:
            P.append('ESPERADOS_v411 nao traz o veredito do ensaio a seco de %s (vereditos_novos_v411): nao ha com que conferir' % k_)
        elif r_.get('verdict') != esp_v_:
            P.append('%s: o veredito do rito difere do ensaio a seco' % k_)
    kf_ = (core.get('kernel_formalization') or {})
    # v411: as QUATRO chaves da v410 (herdadas) seguem LIDAS do kernel do rito, True, com o status nas duas faces; a CHAVE DO LEMA (linked_to_the_corner_by_a_lemma) passa de literal False a leitura True (errata E18); o que fica False por teorema segue False
    rf_ = core.get('rede_fock_v394') or {}
    if rf_.get('whole_certificate_inhabited') is not True:
        P.append('rede_fock_v394: whole_certificate_inhabited deve ser True (lido do kernel do rito: o certificado de Fock esta habitado; errata E14) e o core traz %r' % (rf_.get('whole_certificate_inhabited'),))
    if kf_.get('ext_bin394_0001') is not True:
        P.append('a bandeira da pedra da v394 (ext_bin394_0001) nao segue True no kernel do rito')
    # a face de Fock do psion LE o habitante do certificado (v411): status INHABITED_BY_physicalFockCertificate_V406, habitante exibido, bandeira True e declarada em Psibit.lean
    pb_ = core.get('psibit_v395') or {}; pbc_ = pb_.get('conditional_psion_face') or {}
    if not (pbc_.get('status') == DL_.STATUS_HABITADO and pbc_.get('inhabitant_exhibited') is True and pbc_.get('flag_true') is True and kf_.get(pbc_.get('flag')) is True and pbc_.get('declared_in') == 'TGLExt/Psibit.lean'):
        P.append('psibit_v395: a face do psion nao le o habitante do certificado de Fock como o kernel o diz (status %s, habitante exibido, bandeira True, declarada em TGLExt/Psibit.lean)' % DL_.STATUS_HABITADO)
    fkb_ = ((_base_core(PK).get('testemunha_estatica_v396') or {}).get('fock_face') or {})   # o que a v410 SELADA diz (copia de bytes): o teorema e o modulo da face de Fock, lidos, nao digitados
    te_ = core.get('testemunha_estatica_v396') or {}; fk_ = te_.get('fock_face') or {}; elo_ = fk_.get('elo_v407') or {}
    if not (fk_.get('status') == DL_.STATUS_HABITADO and fk_.get('inhabitant_exhibited') is True and fk_.get('declared_outside_the_stone') == fkb_.get('declared_outside_the_stone') and fk_.get('linked_to_the_corner_by_a_lemma') is True and elo_.get('lemma') == DL_.D7.ANCORA_LEMA and elo_.get('kind') == 'STRUCTURE_NOT_VECTORS' and elo_.get('identifies_omega_with_bell_vector') is False and elo_.get('pair_on_the_fock_face') == 'OPEN' and elo_.get('bell_to_tt_bridge') == 'NOT_A_TERM'
            and fkb_.get('theorem') and fk_.get('theorem') == fkb_.get('theorem') and fkb_.get('declared_in') and fk_.get('declared_in') == fkb_.get('declared_in')):
        P.append('testemunha_estatica_v396: a face de Fock do psion nao le o habitante como o kernel o diz (status %s, habitante exibido) ou a chave do lema (linked_to_the_corner_by_a_lemma) nao e True lida do kernel com o dict elo_v407 (o lema TGLExt.PsionCanto.the_psion_is_the_corner_on_both_faces; elo de ESTRUTURA e nao de vetores; o par na face de Fock ligado na v411 (ParNaFaceDeFock); a ponte Bell-TT NAO e termo)' % DL_.STATUS_HABITADO)
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
    if not (tv_.get('all_verified') is True and tv_.get('does_not_gate_core') is True and len(ck_) == EV_.get('n_checks') and V['veracidade']['checks_ok'] and nums_ok_ and fontes_ok_ and tv_.get('verdict') == (ESP.get('vereditos_v410') or {}).get('teste_de_veracidade_fase9_v397')):
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
                P.append('os numeros que o registro leu != os do resultado pinado (lidos pelos mesmos caminhos de delta_v411.F9_CAMINHOS)')
        if QV_.Q._v397_atomos(tv_, 'pt').get('sealed') is not True or QV_.Q._v397_atomos(tv_, 'en').get('sealed') is not True:
            P.append('o quadro do Teste da Unica Palavra nao sela (algum numero ausente ou o registro nao selou): o artigo diria que o registro nao selou')
    except Exception as e_:   # noqa: BLE001
        P.append('nao consegui conferir o registro do Teste da Unica Palavra contra o resultado pinado: %r' % (e_,))
    # v411: o trio, o axiom_report e a proveniencia do kernel do rito (as OITO ANCORAS do fecho e as bandeiras do bundle, abaixo); nenhum numero e' digitado
    TRIO_ = {'propext', 'Classical.choice', 'Quot.sound'}
    axr_ = kf_.get('axiom_report') or {}; src_ = kf_.get('declaration_sources_v394') or {}
    em_trio_ = lambda n_: bool(isinstance(axr_.get(n_), list) and set(axr_.get(n_)) <= TRIO_)
    V['h8'] = len(kf_.get('formal_files_sha256') or {})
    if V['h8'] != ESP.get('h8_entradas') or not all(r_ in (kf_.get('formal_files_sha256') or {}) for r_ in (ESP.get('h8_residuais_do_nos') or [])):
        P.append('o hash formal do rito tem %s entradas (ESPERADOS[h8_entradas] = %s) ou lhe falta um residual do Nos' % (V['h8'], ESP.get('h8_entradas')))
    # v411: NENHUMA ancora nova e NENHUMA bandeira nova (o kernel e' o da v410): o axiom_report e as bandeiras ext_* True do rito == as da v410 SELADA (base_v410, copia de bytes); o FLAGS_v411.json e o CANDIDATO_v411.json dizem zero bandeira
    kfb_ = _base_core(PK).get('kernel_formalization') or {}
    ext_ = lambda k_: {n_ for n_, v_ in (k_ or {}).items() if str(n_).startswith('ext_') and v_ is True}
    V['ancoras'] = {}; V['ancoras_aescala'] = {}
    iguais_ = {'axiom_report': (kf_.get('axiom_report') or {}) == (kfb_.get('axiom_report') or {}), 'bandeiras_ext': ext_(kf_) == ext_(kfb_), 'escada': ESP['escada'][1] == ESP['escada_v410_e_v411'][0]}
    flags_ = FJ_.get('flags') or []
    V['bandeiras'] = {'n': 0, 'n_true': 0, 'ok': bool(all(iguais_.values()) and not flags_ and FJ_.get('n_flags') == 0 == CM.get('n_bandeiras')), 'por_grupo': {}, 'iguais_a_v410': iguais_}
    if not V['bandeiras']['ok']:
        P.append('o kernel da v411 nao e\' o da v410 (axiom_report, bandeiras ext_* True, escada: %s) ou o FLAGS_v411.json/CANDIDATO_v411.json trazem bandeira nova (FLAGS %s, CANDIDATO %s): a v411 nao tem modulo nem bandeira nova' % (iguais_, FJ_.get('n_flags'), CM.get('n_bandeiras')))
    prov_ = kf_.get('declaration_sources_status_v394') or {}
    if not (prov_.get('ok') is True and prov_.get('compiler_names') == prov_.get('audited_names') == V['axiom_report_n']):
        P.append('a proveniencia emitida pelo compilador nao cobre o axiom_report do rito')
    V['n_bandeiras'] = FJ_['n_flags']; V['n_bandeiras_por_pedra'] = {}   # (v411: zero bandeira nova; o FLAGS_v411.json nao tem por_grupo_bandeiras)
    # as ancoras da IALD2 e da AEscala (v410), as 82 do traducao_turing_v409, as 48 do tetelestai_terminal_v408, as 76 do psion_canto_v407 e as OITO do fechamento_v406 (HERDADAS) seguem no kernel do rito (a v411 NAO acrescenta ancora): lidas dos deltas (delta_v410 e anteriores), nao do ESPERADOS; no trio e declaradas no modulo esperado
    for ak_, aesp_, adesc_ in (('ancoras410', dict(DL_.D10.ANCORAS, **DL_.D10.ANCORAS_AESCALA), 'as ancoras da IALD2 e da AEscala (os registros da v410, recriados)'), ('ancoras409', DL_.D9.ANCORAS, 'as ancoras do traducao_turing_v409 (herdadas)'), ('ancoras408', DL_.D8.ANCORAS, 'as ancoras do tetelestai_terminal_v408 (herdadas)'),
                               ('ancoras407', DL_.D7.ANCORAS, 'as ancoras do psion_canto_v407 (herdadas)'), ('ancoras406', DL_.D6.ANCORAS, 'as oito ancoras do fechamento_v406 (herdadas)')):
        V[ak_] = {n_: {'rel': e_.get('rel'), 'axioms': axr_.get(n_), 'source': src_.get(n_), 'ok': bool(em_trio_(n_) and src_.get(n_) == e_.get('rel'))} for n_, e_ in aesp_.items()}
        if not aesp_ or any(a_['ok'] is not True for a_ in V[ak_].values()):
            P.append('%s deixaram de estar no kernel do rito (no trio, declaradas no modulo esperado): %d de %d' % (adesc_, sum(1 for a_ in V[ak_].values() if a_['ok'] is True), len(aesp_)))
    ft6_ = ESP.get('flags_true_v410') or []
    V['bandeiras410'] = {'n': len(ft6_), 'n_true': sum(1 for f_ in ft6_ if kf_.get(f_) is True)}; V['bandeiras410']['ok'] = bool(ft6_ and V['bandeiras410']['n'] == V['bandeiras410']['n_true'])
    if not V['bandeiras410']['ok']:
        P.append('alguma bandeira True da v410 deixou de ser True no kernel do rito (%s de %s): a v411 so\' acrescenta' % (V['bandeiras410']['n_true'], V['bandeiras410']['n']))
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
    # o registro h0dn_bg1_v411 (o UNICO registro NOVO com FUNCAO; o teste H0DN x BG1 ABERTO UMA VEZ, D169): le-se pela funcao _ler_fecho_v411 (conferida contra ESPERADOS[registros_funcao_v411][h0dn], o selo e o stdout; fail-closed); o gate nao se move
    import guarda_frases_v411 as GFH_
    from guarda_p18_v411 import violacoes as P18H_
    out_n_ = out.replace('\r\n', '\n')
    V['fecho'], P_f_ = _ler_fecho_v411(core, ESP, CM, selo, out_n_, DL_, GFH_, P18H_, b0_)
    P.extend(P_f_)
    # o registro traducao_turing_v409 (HERDADO da v410, RECRIADO pelo rito da v411; a escada do contrato subida pela C12, veredito na troca dita): segue SELADO; as checagens da v410, os valores (as ancoras, os 2 modulos, as bandeiras, a escada, o gate) == ESPERADOS[registros_funcao_v410][traducao_turing],
    # NENHUMA chave antiga muda, o acervo da v407 na copia purgada (D57d da v410), as respostas do operador de 05/11, o beta em runtime, as ressalvas da v410 e a linha do bloco no stdout
    t9_ = core.get('traducao_turing_v409') or {}; t9_m_ = t9_.get('mechanics') or {}; t9_v_ = t9_.get('values') or {}; ET9_ = ((ESP.get('registros_funcao_v409') or {}).get(DL_.D9.TESTEMUNHA['key']) or (ESP.get('registros_funcao_v410') or {}).get(DL_.D9.TESTEMUNHA['key'])) or {}; rs9_ = t9_v_.get('respostas') or {}; ac9_ = t9_.get('acervo_v407_repinado') or {}
    N9F_ = (ET9_.get('values') or {}).get('n_flags')   # o numero das bandeiras do bundle da v410: lido de ESPERADOS[registros_funcao_v410] (o ensaio a seco), nunca digitado
    t9_mech_ok_ = bool(t9_m_.get('passed') is True and t9_m_.get('n_checks') == DL_.D9.N_CHECKS_FECHO == ET9_.get('n_checks') == len(t9_m_.get('checks') or []) and all(c_.get('ok') is True for c_ in (t9_m_.get('checks') or [])))
    t9_values_ok_ = bool(t9_v_.get('n_ancoras_ok') == t9_v_.get('n_ancoras') == len(DL_.D9.ANCORAS) and bool(DL_.D9.ANCORAS) and t9_v_.get('n_modulos_ok') == t9_v_.get('n_modulos') == DL_.D9.N_BUNDLE and t9_v_.get('n_flags_true') == t9_v_.get('n_flags') == N9F_ and isinstance(N9F_, int) and t9_v_.get('escada') == [ESP['escada'][1]] * 3
                         and t9_v_.get('gate_verdict') == ESP.get('qg_closure_gate_verdict_v410') == selo.get('qg_closure_verdict') and t9_v_.get('fica_false_por_teorema') == list(DL_.FICAM_FALSE_POR_TEOREMA) and t9_v_.get('ressalvas') == list(DL_.D9.RESSALVAS_V409) and list(t9_.get('ressalvas') or []) == list(DL_.D9.RESSALVAS_V409)
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
                  and t9_mech_ok_ and t9_values_ok_ and t9_ac_ok_ and t9_resp_ok_ and t9_beta_ok_ and t9_anc_ok_ and V['bundle409']['ok'] and all(a_['ok'] for a_ in V['ancoras409'].values()) and t9_std_ok_ and not t9_.get('guarda_violacoes')   # (o traducao_turing_v409 le o bundle e as ancoras DELE: v409; V['bundle410'] e V['ancoras410'] sao os da v410) [12/11, claude-construtor-v411-posrito: a condicao que o comentario engolia (achado do agente H) voltou ao codigo]
                  and not GUARDA.search(str(t9_.get('verdict') or '')))
    V['fecho410'] = {'registro': 'traducao_turing_v409', 'verdict': t9_.get('verdict'), 'ok': t9_.get('all_verified'), 'sealed': t9_ok_, 'n_checks': t9_m_.get('n_checks'), 'mech_ok': t9_mech_ok_, 'values': t9_v_, 'values_ok': t9_values_ok_, 'beta_ok': t9_beta_ok_, 'ancoras_ok': t9_anc_ok_,
                     'stdout_ok': t9_std_ok_, 'runtime_executed': t9_.get('runtime_executed'), 'does_not_gate_core': t9_.get('does_not_gate_core'), 'ancora_principal': t9_.get('ancora_principal'), 'chaves_antigas_que_mudam': t9_.get('chaves_antigas_que_mudam'), 'acervo_ok': t9_ac_ok_, 'respostas_ok': t9_resp_ok_}
    if not t9_ok_:
        P.append('traducao_turing_v409 (HERDADO, recriado) nao selou inteiro (selo, as %s checagens do registro, valores [%s ancoras, %s modulos, as bandeiras da v410, escada, gate] == os de ESPERADOS[registros_funcao_v410], NENHUMA chave antiga muda, o acervo da v407 na copia purgada, as respostas do operador de 05/11, beta == alfa x raiz de e do core, '
                 'as ressalvas da v410, o bundle da v410 [%s], a linha do bloco A TRADUCAO AS CLASSES DE TURING no stdout, nao move o gate): ver o registro no core' % (DL_.D9.N_CHECKS_FECHO, len(DL_.D9.ANCORAS), DL_.D9.N_BUNDLE, DL_.D9.N_BUNDLE))
    # o registro tetelestai_terminal_v408 (HERDADO da v408, RECRIADO pelo rito da v411; a escada do contrato subida pela C12, veredito na troca dita): segue SELADO; as 16 checagens, os valores (as 48 ancoras, os 4 modulos, as 71 bandeiras, a escada, o gate) == ESPERADOS[registros_funcao_v408], NENHUMA chave antiga muda, o insumo purgado (E23 da v408), as respostas do operador de 04/11, o beta em runtime, as ressalvas da v408 e a linha do bloco no stdout
    t8_ = core.get('tetelestai_terminal_v408') or {}; t8_m_ = t8_.get('mechanics') or {}; t8_v_ = t8_.get('values') or {}; ET8_ = (ESP.get('registros_funcao_v408') or {}).get('tetelestai_terminal') or {}; ip8_ = t8_.get('insumo_purgado') or {}; ip8v_ = t8_v_.get('insumo_purgado') or {}; rs8_ = t8_v_.get('respostas') or {}
    N8F_ = (ET8_.get('values') or {}).get('n_flags')   # o numero das bandeiras do bundle da v410 (71): lido de ESPERADOS[registros_funcao_v408] (o ensaio a seco), nunca digitado
    t8_mech_ok_ = bool(t8_m_.get('passed') is True and t8_m_.get('n_checks') == DL_.D8.N_CHECKS_FECHO == ET8_.get('n_checks') == len(t8_m_.get('checks') or []) and all(c_.get('ok') is True for c_ in (t8_m_.get('checks') or [])))
    t8_values_ok_ = bool(t8_v_.get('n_ancoras_ok') == t8_v_.get('n_ancoras') == len(DL_.D8.ANCORAS) and bool(DL_.D8.ANCORAS) and t8_v_.get('n_modulos_ok') == t8_v_.get('n_modulos') == DL_.D8.N_BUNDLE and t8_v_.get('n_flags_true') == t8_v_.get('n_flags') == N8F_ and isinstance(N8F_, int) and t8_v_.get('escada') == [ESP['escada'][1]] * 3
                         and t8_v_.get('gate_verdict') == ESP.get('qg_closure_gate_verdict_v410') == selo.get('qg_closure_verdict') and t8_v_.get('fica_false_por_teorema') == list(DL_.FICAM_FALSE_POR_TEOREMA) and t8_v_.get('ressalvas') == list(DL_.D8.RESSALVAS_V408) and list(t8_.get('ressalvas') or []) == list(DL_.D8.RESSALVAS_V408)
                         and bool(ET8_.get('values')) and _feq({kk_: t8_v_.get(kk_) for kk_ in ET8_['values']}, ET8_['values']))
    t8_ip_ok_ = bool(ip8v_.get('ok') is True and ip8v_.get('sha256') == ip8_.get('sha256') == DL_.D8.PURGADO_SHA256 and ip8v_.get('integra_nao_pinada') is True and ip8_.get('integra_pinada') is False and ip8_.get('integra_fora_do_espelho') is True)
    t8_resp_ok_ = bool(rs8_ and set(rs8_) == {r_['id'] for r_ in DL_.D8.RESPOSTAS_DO_OPERADOR} and all(v_ is True for v_ in rs8_.values()) and t8_v_.get('respostas_ok') is True)
    t8_beta_ok_ = bool(t8_.get('beta_ok') is True and isinstance(t8_v_.get('beta'), float) and isinstance(b0_, float) and abs(t8_v_['beta'] - b0_) <= 1e-9 * abs(b0_))
    t8_anc_ok_ = bool(len(t8_.get('anchors') or {}) == len(DL_.D8.ANCORAS) and all(a_ is True for a_ in (t8_.get('anchors') or {}).values()) and set(t8_.get('anchors') or {}) == set(DL_.D8.ANCORAS) == set(t8_v_.get('ancoras') or {}) and all((a_ or {}).get('ok') is True for a_ in (t8_v_.get('ancoras') or {}).values()))
    m_t8_ = re.search(r'ancoras ok = (\d+)/(\d+) ; modulos do bundle ok = (\d+)/(\d+) ; bandeiras True = (\d+)/(\d+) ; escada = (\[.*?\]) ; gate = (.*)$', out, flags=re.M)   # a linha do bloco TETELESTAI E' O TERMINAL (herdado): sem «chave do lema» e sem «certificado habitado»; «modulos» no plural (a da v411 diz «modulo»)
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
    # o registro psion_canto_v407 (HERDADO da v407, RECRIADO pelo rito da v411; a escada do contrato subida pela C12, veredito na troca dita): segue SELADO; as 16 checagens, os valores (as 76 ancoras, os 9 modulos, as 98 bandeiras, a escada, o gate) == ESPERADOS[registros_funcao_v407], a CHAVE DO LEMA lida do kernel, as cinco chaves iguais as da v410 selada, o que fica False por teorema, o beta em runtime, as ressalvas da v410, o teste (d) so' citado e a linha do bloco no stdout
    pc_ = core.get('psion_canto_v407') or {}; pc_m_ = pc_.get('mechanics') or {}; pc_v_ = pc_.get('values') or {}; pc_k_ = pc_.get('keys') or {}; EPC_ = (ESP.get('registros_funcao_v407') or {}).get('psion_canto') or {}; td_ = pc_.get('teste_d') or {}
    N7F_ = (EPC_.get('values') or {}).get('n_flags')   # o numero das bandeiras do bundle da v407 (98): lido de ESPERADOS[registros_funcao_v407] (o ensaio a seco), nunca digitado
    pc_mech_ok_ = bool(pc_m_.get('passed') is True and pc_m_.get('n_checks') == DL_.D7.N_CHECKS_FECHO == EPC_.get('n_checks') == len(pc_m_.get('checks') or []) and all(c_.get('ok') is True for c_ in (pc_m_.get('checks') or [])))
    pc_values_ok_ = bool(pc_v_.get('n_ancoras_ok') == pc_v_.get('n_ancoras') == len(DL_.D7.ANCORAS) and bool(DL_.D7.ANCORAS) and pc_v_.get('n_modulos_ok') == pc_v_.get('n_modulos') == DL_.D7.N_BUNDLE and pc_v_.get('n_flags_true') == pc_v_.get('n_flags') == N7F_ and isinstance(N7F_, int) and pc_v_.get('escada') == [ESP['escada'][1]] * 3
                         and pc_v_.get('gate_verdict') == ESP.get('qg_closure_gate_verdict_v410') == selo.get('qg_closure_verdict') and pc_v_.get('elo_lido_do_kernel') is True and pc_v_.get('fica_false_por_teorema') == list(DL_.FICAM_FALSE_POR_TEOREMA) and pc_v_.get('ressalvas') == list(DL_.D7.RESSALVAS_V407) and list(pc_.get('ressalvas') or []) == list(DL_.D7.RESSALVAS_V407)
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
    # o registro fechamento_v406 (HERDADO da v406, RECRIADO pelo rito da v411; a checagem c8 versionada pela errata E20 desde a v410): segue SELADO e de veredito esperado (ESPERADOS[registros_funcao_v406]); as 14 checagens, os valores, as OITO ancoras, os 301 modulos, as 1794 bandeiras, as QUATRO chaves (a do lema True) e a linha do bloco no stdout
    fe_ = core.get('fechamento_v406') or {}; fe_m_ = fe_.get('mechanics') or {}; fe_v_ = fe_.get('values') or {}; fk4_ = fe_.get('four_keys') or {}; EFE_ = (ESP.get('registros_funcao_v406') or {}).get('fechamento') or {}
    N6F_ = (EFE_.get('values') or {}).get('n_flags')   # o numero das bandeiras do bundle da v406 (1794): lido de ESPERADOS[registros_funcao_v406] (o ensaio a seco), nunca digitado
    fe_mech_ok_ = bool(fe_m_.get('passed') is True and fe_m_.get('n_checks') == DL_.D6.N_CHECKS_FECHO == EFE_.get('n_checks') == len(fe_m_.get('checks') or []) and all(c_.get('ok') is True for c_ in (fe_m_.get('checks') or [])))
    fe_values_ok_ = bool(fe_v_.get('n_ancoras_ok') == len(DL_.D6.ANCORAS) and bool(DL_.D6.ANCORAS) and fe_v_.get('n_modulos_ok') == fe_v_.get('n_modulos') == DL_.D6.N_BUNDLE and fe_v_.get('n_flags_true') == fe_v_.get('n_flags') == N6F_ and isinstance(N6F_, int) and fe_v_.get('escada') == [ESP['escada'][1]] * 3
                         and fe_v_.get('gate_verdict') == ESP.get('qg_closure_gate_verdict_v410') == selo.get('qg_closure_verdict') and fe_v_.get('certificado_habitado_lido_do_kernel') is True and fe_v_.get('fica_false_por_teorema') == list(DL_.FICAM_FALSE_POR_TEOREMA)
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
                  and fe_mech_ok_ and fe_values_ok_ and fe_chaves_ok_ and fe_beta_ok_ and fe_anc_ok_ and V['bundle406']['ok'] and V['bandeiras410']['ok'] and all(a_['ok'] for a_ in V['ancoras406'].values()) and fe_std_ok_ and not fe_.get('guarda_violacoes')
                  and fe_.get('nome_provisorio_da_candidata') == DL_.D6.TESTEMUNHA['nome_provisorio_da_gerencia'] and not GUARDA.search(str(fe_.get('verdict') or '')))
    V['fecho406'] = {'registro': 'fechamento_v406', 'verdict': fe_.get('verdict'), 'ok': fe_.get('all_verified'), 'sealed': fe_ok_, 'n_checks': fe_m_.get('n_checks'), 'mech_ok': fe_mech_ok_, 'values': fe_v_, 'values_ok': fe_values_ok_, 'chaves_ok': fe_chaves_ok_, 'beta_ok': fe_beta_ok_, 'ancoras_ok': fe_anc_ok_,
                     'stdout_ok': fe_std_ok_, 'certificado_habitado': fe_.get('certificate_inhabited'), 'runtime_executed': fe_.get('runtime_executed'), 'does_not_gate_core': fe_.get('does_not_gate_core'), 'nome_provisorio': fe_.get('nome_provisorio_da_candidata')}
    V['chaves406'] = dict(fk4_)
    if not fe_ok_:
        P.append('fechamento_v406 (HERDADO, recriado) nao selou inteiro (selo, as %s checagens do registro [a c8 VERSIONADA pela errata E20], valores [8 ancoras, 301 modulos, 1794 bandeiras, escada, gate] == os de ESPERADOS[registros_funcao_v406], as quatro chaves LIDAS do kernel [True; status %s; o lema agora True; as duas que ficam False por teorema, False], beta == alfa x raiz de e do core, '
                 'as ressalvas da v410, o nome provisorio da candidata, o bundle da v410 [301], as bandeiras da v410 [todas True], a linha do bloco O FECHAMENTO no stdout, nao move o gate): ver o registro no core' % (DL_.D6.N_CHECKS_FECHO, DL_.STATUS_HABITADO))
    # a errata de F2b (registro com FUNCAO, SEM pedra): o V1 do ramo B lido por hash e como antes, o livro v383 intacto, a calibracao A e a previsao do par LIDAS do V1, a previsao fora do intervalo de A e de sinal oposto, nenhum desfecho; o canal passa de AWAITING a retirado antes do dado AO LADO
    fb_ = core.get('f2b_errata_v404') or {}; EFB_ = RF4_.get('f2b') or {}; fbm_ = fb_.get('mechanics') or {}; fbv_ = fb_.get('values') or {}
    rbc_ = core.get('ramo_b_preregistration_v386') or {}; ldc_ = (core.get('ledger_errata_v386') or {}).get('charge_F2b') or {}; rbb_ = _base_core(PK).get('ramo_b_preregistration_v386') or {}; ldb_ = (_base_core(PK).get('ledger_errata_v386') or {}).get('charge_F2b') or {}
    f2b_mech_ok_ = bool(fbm_.get('passed') is True and fbm_.get('n_checks') == DL_.D4.N_CHECKS['f2b'] == EFB_.get('n_checks') and len(fbm_.get('checks') or []) == DL_.D4.N_CHECKS['f2b'] and all(c_.get('ok') is True for c_ in (fbm_.get('checks') or [])))
    f2b_values_ok_ = bool(fbv_ and EFB_.get('values') and set(EFB_['values']) <= set(fbv_) and _feq({kk_: fbv_.get(kk_) for kk_ in EFB_['values']}, EFB_['values']))
    f2b_beta_ok_ = bool(fb_.get('beta_ok') is True and isinstance(fbv_.get('beta'), float) and isinstance(b0_, float) and abs(fbv_['beta'] - b0_) <= 1e-9 * abs(b0_))
    f2b_ao_lado_ok_ = bool(fb_.get('F2b_status_before') == 'AWAITING' and fb_.get('F2b_status_now') == DL_.D4.F2B_FUTURO_TOKEN == (ESP.get('f2b_depois') or {}).get('F2b_status_now') and fb_.get('channel_token_now') == DL_.D4.F2B_FUTURO_TOKEN and fb_.get('v1_token_kept') == DL_.D4.F2B_V1_TOKEN_ANTIGO
                           and rbc_.get('F2b_status') == (ESP.get('f2b_antes') or {}).get('F2b_status') and rbc_.get('veredito_do_V1') == (ESP.get('f2b_antes') or {}).get('veredito_do_V1') and bool(rbb_) and _feq(rbc_, rbb_) and bool(ldb_) and _feq(ldc_, ldb_) and ldc_.get('token') == (ESP.get('f2b_antes') or {}).get('charge_F2b_token'))
    nmc_ = core.get('neutrino_mass') or {}
    neutrino_intacto_ = bool(hashlib.sha256(str(nmc_.get('angle_status') or '').encode('utf-8')).hexdigest() == ESP.get('neutrino_angle_status_antigo_sha256') and nmc_.get('frozen_hash') == ESP.get('neutrino_frozen_hash_v410') and nmc_.get('verdict') == (ESP.get('vereditos_v410') or {}).get('neutrino_mass'))
    f2b_ok_ = bool(fb_.get('all_verified') is True and fb_.get('does_not_gate_core') is True and fb_.get('runtime_executed') is True and bool(EFB_.get('verdict')) and fb_.get('verdict') == EFB_.get('verdict') and f2b_mech_ok_ and f2b_values_ok_ and f2b_beta_ok_ and f2b_ao_lado_ok_ and neutrino_intacto_
                   and not fb_.get('guarda_p18_violacoes') and not GUARDA.search(str(fb_.get('verdict') or '')))
    V['f2b'] = {'registro': 'f2b_errata_v404', 'verdict': fb_.get('verdict'), 'ok': fb_.get('all_verified'), 'sealed': f2b_ok_, 'n_checks': fbm_.get('n_checks'), 'mech_ok': f2b_mech_ok_, 'values': fbv_, 'values_ok': f2b_values_ok_, 'beta_ok': f2b_beta_ok_, 'ao_lado_ok': f2b_ao_lado_ok_,
                'neutrino_intacto': neutrino_intacto_, 'status_antes': fb_.get('F2b_status_before'), 'status_agora': fb_.get('F2b_status_now'), 'token_v1': fb_.get('v1_token_kept'), 'runtime_executed': fb_.get('runtime_executed'), 'does_not_gate_core': fb_.get('does_not_gate_core')}
    if not f2b_ok_:
        P.append('f2b_errata_v404 nao selou inteiro (selo, as %s checagens do registro, valores == ESPERADOS[registros_funcao_v410][f2b], beta == alfa x raiz de e do core, o V1 do ramo B, o registro da v386 e a cobranca F2b da v386 IGUAIS aos da v410 selada [a errata e\' AO LADO], o canal agora retirado antes do dado, '
                 'a funcao do neutrino intacta [angle_status antigo, frozen_hash e veredito], nenhum desfecho, nao move o gate): ver o registro no core' % DL_.D4.N_CHECKS['f2b'])
    # as BANDEIRAS DO GATE (F8.1 da v410; registro com FUNCAO bandeiras_do_gate_v403, RECRIADO pelo rito da v411): conferido por inteiro contra ESPERADOS[registros_funcao_v410][gate] (as checagens e os valores == os do core da v410 selada) e RELIDO aqui no core do rito, independente do registro (as tres fontes das bandeiras antes literais, os seis checks do gate da v410 mais a sonda, a letra do veredito)
    gk_ = core.get('bandeiras_do_gate_v403') or {}; EG_ = RF3_.get('gate') or {}; gm_ = gk_.get('mechanics') or {}; gv_ = gk_.get('values') or {}
    gmech_ok_ = bool(gm_.get('passed') is True and gm_.get('n_checks') == DL_.D3.N_CHECKS['gate'] == EG_.get('n_checks') and len(gm_.get('checks') or []) == DL_.D3.N_CHECKS['gate'] and all(c_.get('ok') is True for c_ in (gm_.get('checks') or [])))
    gvalues_ok_ = bool(gv_ and EG_.get('values') and set(EG_['values']) <= set(gv_) and _feq({kk_: gv_.get(kk_) for kk_ in EG_['values']}, EG_['values']))
    qgx_ = core.get('qg_closure') or {}
    n18x_ = sum(1 for fam_ in ('formal_flags', 'physics_flags', 'experiment_flags') for v_ in (qgx_.get(fam_) or {}).values() if v_ is True)
    ls2x_ = sorted(k_ for k_ in kf_ if k_.startswith(DL_.F81_PREFIXO_LS2))
    prex_ = [c_[1] for c_ in ((core.get('void_floor_v11') or {}).get('checks') or []) if isinstance(c_, (list, tuple)) and len(c_) == 2 and c_[0] == DL_.F81_ROTULO_PREREG]
    ck_old_ = [list(c_) for c_ in (ESP.get('qg_closure_v410_checks') or [])]; ck_new_ = [list(c_) for c_ in (qgx_.get('checks') or [])]
    sonda_ = [c_ for c_ in ck_new_ if str(c_[0]).startswith('ProbeBlindNullAbsent')]
    f81x_ok_ = bool(len(ls2x_) == 6 and all(kf_.get(k_) is True for k_ in ls2x_) and (qgx_.get('physics_flags') or {}).get('linearized_spin2_finite_face') is True and len(prex_) == 1 and prex_[0] is True and (qgx_.get('experiment_flags') or {}).get('protocol_pre_registered') is True
                    and (core.get('void_stacking_blind') or {}).get('all_verified') is True and (qgx_.get('experiment_flags') or {}).get('null_tests_passed_blind') is True and n18x_ == 18
                    and len(ck_old_) == 7 and ck_new_ == ck_old_ and len(sonda_) == 1 and all(c_[1] is True for c_ in ck_new_)
                    and (qgx_.get('gate') or {}).get('verdict') == ESP.get('qg_closure_gate_verdict_v410') == selo.get('qg_closure_verdict'))
    gate_ok_ = bool(gk_.get('all_verified') is True and gk_.get('does_not_gate_core') is True and gk_.get('runtime_executed') is True and bool(EG_.get('verdict')) and gk_.get('verdict') == EG_.get('verdict') and gmech_ok_ and gvalues_ok_ and f81x_ok_
                    and gv_.get('n_flags') == 18 == gv_.get('n_true') == gv_.get('n_calculated') and gv_.get('n_literal') == 0 and gv_.get('n_read_by_the_verdict') == 15 and gv_.get('read_by_the_verdict') == [6, 5, 4] and gv_.get('gate_verdict_equals_v402') is True
                    and not GUARDA.search(str(gk_.get('verdict') or '')))
    V['gate'] = {'registro': 'bandeiras_do_gate_v403', 'verdict': gk_.get('verdict'), 'ok': gk_.get('all_verified'), 'sealed': gate_ok_, 'n_checks': gm_.get('n_checks'), 'mech_ok': gmech_ok_, 'values': gv_, 'values_ok': gvalues_ok_, 'f81_ok': f81x_ok_, 'n18': n18x_, 'n_ls2': len(ls2x_),
                 'n_checks_do_gate': len(ck_new_), 'sonda': len(sonda_), 'runtime_executed': gk_.get('runtime_executed'), 'does_not_gate_core': gk_.get('does_not_gate_core')}
    if not gate_ok_:
        P.append('bandeiras_do_gate_v403 nao selou inteiro (selo, as %s checagens do registro, valores == ESPERADOS[registros_funcao_v410][gate], 18 bandeiras True e TODAS calculadas, 15 no veredito (6+5+4), a releitura aqui das tres fontes da F8.1 [a familia ext_ls2_* do kernel, a checagem «pre-registro v67 INTACTO (hash)» do rito V11, o teste nulo cego], '
                 'os sete checks do gate (os seis da v410 mais a sonda ProbeBlindNullAbsent) IGUAIS aos da v410 selada, a letra do veredito do gate == a da v410 e a do selo, nao move o gate): ver o registro no core' % DL_.D3.N_CHECKS['gate'])
    # os registros com FUNCAO da v402 (ponte, queda, esperanca) e da v410 (caminho, vida, verdade_adendo) RECRIADOS pelo rito: iguais ao que a v410 SELOU (veredito == ESPERADOS[vereditos_v410]; as checagens e os valores do calculo == os do core selado em base_v410), selados, com a composicao e a estrela no kernel do rito e no trio
    for fkey_, FUN_ in (('fun402', FUN_V402), ('fun410', FUN_V410), ('fun410b', FUN_V410B), ('fun410c', FUN_V410C)):
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
                P.append('%s nao selou inteiro (recriado pelo rito: selo, veredito == o da v410 selada, as checagens e os valores do calculo == os da v410 selada [base_v410], beta == alfa x raiz de e do core, a composicao e a estrela no kernel do rito e no trio, nao move o gate): ver o registro no core' % nome_)
    # as TREZE pedras SELADAS da v403, da v404 e da v410 seguem no kernel do Nos com o sha256 selado (lido do core da v410 selada em base_v410; registro: pedra selada nao se renomeia por cima)
    V['pedras_v408'] = {}
    bkf_ = ((_base_core(PK).get('kernel_formalization') or {}).get('formal_files_sha256')) or {}
    for rel_ in dict.fromkeys(s_['rel'] for D_ in (DL_.D3, DL_.D4, DL_.D5) for s_ in D_.STONES):
        h_ = bkf_.get(rel_); pth_ = os.path.join(NOS, 'tgl_kernel', *rel_.split('/')); shaf_ = sha(pth_) if os.path.isfile(pth_) else None
        V['pedras_v408'][rel_] = {'sha16': (shaf_ or '')[:16], 'ok': bool(h_ and shaf_ == h_ and (kf_.get('formal_files_sha256') or {}).get(rel_) == h_)}
    if len(V['pedras_v408']) != 13 or any(p_['ok'] is not True for p_ in V['pedras_v408'].values()):
        P.append('as treze pedras seladas (v403: 3, v404: 2, v410: 8) deixaram de estar no kernel do Nos com o sha256 selado (registro: pedra selada nao se renomeia por cima): %d lidas' % len(V['pedras_v408']))
    # a falsidade da inercia (v401, registro com FUNCAO) RECRIADA pelo rito: igual ao ensaio a seco (veredito) e a v410 SELADA (valores e checagens do calculo), com a composicao e a estrela no kernel do rito
    fa_ = core.get('falsidade_da_inercia_v401') or {}; fm_ = fa_.get('mechanics') or {}; fvv_ = fa_.get('values') or {}
    fab_ = _base_core(PK).get('falsidade_da_inercia_v401') or {}   # a falsidade da v410 SELADA (copia de bytes em base_v410): a recriada tem de dar os mesmos valores
    values_f_ok_ = bool(fvv_ and (fab_.get('values') or {}) and _feq(fvv_, fab_['values']) and _feq(fm_, fab_.get('mechanics')))
    mech_ok_ = bool(fm_.get('passed') is True and fm_.get('n_checks') == DL_.N_CHECKS_FALSIDADE and len(fm_.get('checks') or []) == DL_.N_CHECKS_FALSIDADE and all(c_.get('ok') is True for c_ in (fm_.get('checks') or [])))
    beta_f_ok_ = bool(fa_.get('beta_ok') is True and isinstance(fvv_.get('beta'), float) and isinstance(b0_, float) and abs(fvv_['beta'] - b0_) <= 1e-9 * abs(b0_))
    hy_ = fa_.get('named_hypothesis') or {}
    chain_ok_ = bool('DERIVED' in str(fa_.get('chain_status')) and hy_.get('name') == 'H_tau' and hy_.get('status') == 'OPEN' and hy_.get('used_by_a_theorem') is False and isinstance(fvv_.get('min_weight_on_the_grid_positive'), float) and fvv_['min_weight_on_the_grid_positive'] > 0.0
                     and fvv_.get('diag_flow_gap_zero_is_fixed') is True and bool(fvv_.get('abyss_witnesses')) and bool(fvv_.get('leak_witnesses_g_half')))
    fu_ = fa_.get('unconditional') or {}; fkt_ = fa_.get('key_theorem') or {}
    kernel_f_ok_ = bool(fu_.get('in_kernel') is True and fkt_.get('in_kernel') is True and fu_.get('theorem') and fkt_.get('theorem') and kf_.get(fu_.get('flag')) is True and kf_.get(fkt_.get('flag')) is True and em_trio_(fu_.get('theorem')) and em_trio_(fkt_.get('theorem')))
    fal_ok_ = bool(chain_ok_ and fa_.get('all_verified') is True and fa_.get('does_not_gate_core') is True and fa_.get('runtime_executed') is True and bool(ESP.get('veredito_da_falsidade_v410')) and fa_.get('verdict') == ESP.get('veredito_da_falsidade_v410') and mech_ok_ and values_f_ok_ and beta_f_ok_
                   and (fa_.get('costless') or {}).get('ok') is True and kernel_f_ok_ and not GUARDA.search(str(fa_.get('verdict') or '')))
    V['fal401'] = {'verdict': fa_.get('verdict'), 'ok': fa_.get('all_verified'), 'sealed': fal_ok_, 'n_checks': fm_.get('n_checks'), 'mech_ok': mech_ok_, 'values_ok': values_f_ok_, 'beta_ok': beta_f_ok_, 'chain_ok': chain_ok_, 'kernel_ok': kernel_f_ok_,
                   'costless_ok': (fa_.get('costless') or {}).get('ok'), 'runtime_executed': fa_.get('runtime_executed'), 'does_not_gate_core': fa_.get('does_not_gate_core')}
    if not fal_ok_:
        P.append('falsidade_da_inercia_v401 nao selou inteiro (recriada pelo rito: selo, as checagens do calculo no modelo oneScaling (DL.N_CHECKS_FALSIDADE), a cadeia derivada [DERIVED], a hipotese H_tau [OPEN] nao usada por teorema, valores e checagens == os da v410 selada, beta == alfa x raiz de e do core, 0_abs de costless no kernel embutido, a composicao e a estrela no kernel do rito, nao move o gate): ver o registro no core')
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
    sr_ = selo.get('selo_pela_propria_tecnologia_v399') or {}; sdr_ = selo.get('declaracao_do_operador_v399') or {}; sreg_ = selo.get('registros_v399') or {}; sfr_ = selo.get('falsidade_da_inercia_v401') or {}; sreg1_ = selo.get('registros_v401') or {}; sreg2_ = selo.get('registros_v402') or {}; sreg3_ = selo.get('registros_v403') or {}; sreg4_ = selo.get('registros_v404') or {}; sreg5_ = selo.get('registros_v405') or {}; sreg6_ = selo.get('registros_v406') or {}; sreg7_ = selo.get('registros_v407') or {}; sreg8_ = selo.get('registros_v408') or {}; sreg9_ = selo.get('registros_v409') or {}; sreg10_ = selo.get('registros_v411') or {}   # (os DOIS por spec NOVOS da v411; os da v410 seguem em selo['registros_v410'], inalterados)
    resumos_ok_ = bool(sr_.get('verdict') == sa_.get('verdict') and sr_.get('all_verified') is True and sr_.get('sha256_do_um_py') == V['s64'] and sr_.get('does_not_gate_core') is True and sdr_.get('verdict') == dc_.get('verdict') and sdr_.get('all_verified') is True
                       and sdr_.get('verbatim_sha256') == EDC_.get('verbatim_sha256') and sdr_.get('does_not_gate_core') is True and bool(ESP.get('registros_v399')) and all((sreg_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') for k_ in ESP['registros_v399'])
                       and sfr_.get('verdict') == fa_.get('verdict') and bool(sfr_.get('verdict')) and sfr_.get('all_verified') is True and bool(ESP.get('registros_v401')) and all((sreg1_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and (sreg1_.get(k_) or {}).get('all_verified') is True for k_ in ESP['registros_v401'])
                       and all(((selo.get(n_) or {}).get('verdict') == (core.get(n_) or {}).get('verdict') and bool((selo.get(n_) or {}).get('verdict')) and (selo.get(n_) or {}).get('all_verified') is True and (selo.get(n_) or {}).get('does_not_gate_core') is True) for n_ in tuple(REG_FUNCAO) + tuple(REG_RECRIADOS_V410F) + tuple(FUN_V410B.values()) + ('f2b_errata_v404',) + tuple(FUN_V410.values()) + tuple(FUN_V402.values()) + ('bandeiras_do_gate_v403',) + tuple(FUN_V410C.values()) + ('fechamento_v406', 'psion_canto_v407', 'tetelestai_terminal_v408', 'traducao_turing_v409'))
                       and bool(ESP.get('registros_v402')) and all((sreg2_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg2_.get(k_) or {}).get('verdict')) and (sreg2_.get(k_) or {}).get('all_verified') is True for k_ in ESP['registros_v402'])
                       and bool(ESP.get('registros_v403')) and all((sreg3_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg3_.get(k_) or {}).get('verdict')) and (sreg3_.get(k_) or {}).get('all_verified') is True for k_ in ESP['registros_v403'])
                       and bool(ESP.get('registros_v404')) and all((sreg4_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg4_.get(k_) or {}).get('verdict')) and (sreg4_.get(k_) or {}).get('all_verified') is True for k_ in ESP['registros_v404'])
                       and bool(R410SPEC_) and all((sreg5_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg5_.get(k_) or {}).get('verdict')) and (sreg5_.get(k_) or {}).get('all_verified') is True for k_ in R410SPEC_)
                       and bool(R406DSPEC_) and all((sreg6_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg6_.get(k_) or {}).get('verdict')) and (sreg6_.get(k_) or {}).get('all_verified') is True for k_ in R406DSPEC_)
                       and bool(R407DSPEC_) and all((sreg7_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg7_.get(k_) or {}).get('verdict')) and (sreg7_.get(k_) or {}).get('all_verified') is True for k_ in R407DSPEC_)
                       and bool(R408DSPEC_) and all((sreg8_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg8_.get(k_) or {}).get('verdict')) and (sreg8_.get(k_) or {}).get('all_verified') is True for k_ in R408DSPEC_)
                       and bool(R410TSPEC_) and all((sreg9_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg9_.get(k_) or {}).get('verdict')) and (sreg9_.get(k_) or {}).get('all_verified') is True for k_ in R410TSPEC_)
                       and bool(R411SPEC_) and all((sreg10_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg10_.get(k_) or {}).get('verdict')) and (sreg10_.get(k_) or {}).get('all_verified') is True for k_ in R411SPEC_))
    V['resumos_do_selo_ok'] = resumos_ok_
    if not resumos_ok_:
        P.append('o selo primario (um_absoluto_selo.json) nao traz os resumos do selo ACOM, da declaracao e dos registros por spec iguais aos do core')
    V['formais_nao_selados'] = sorted((selo.get('not_sealed_this_run') or {}).get('formais') or [])
    if V['formais_nao_selados'] != sorted(ESP.get('not_sealed_formais') or []):
        P.append('o selo traz modulo formal nao selado em not_sealed_this_run.formais (a recusa do selo ACOM so registra, mas o rito real tem de selar): %s' % V['formais_nao_selados'][:3])
    # cunhagens_v411 e kh_n1_cobertura_v411 (os DOIS registros por spec NOVOS): as falas do operador de 11 e 12/11 por sha256 (embedded_ok, todas do operador; os textos da gerencia a que ele respondeu so' citados por sha256); as decisoes do delta; E41, E42 e E43 mais a errata ao lado dos pisos de kh_n1_cobertura_v410
    # (todas assinadas pela gerencia c1, em nome proprio: DL.ASSINA); as sete ressalvas por rotulo; o alcance de P = nP; a regra do nome (nenhuma leitura do operador); D65; a MOLDURA (nenhuma frase proibida nos registros novos, inclusive no h0dn_bg1_v411); a cobertura do Audit (nenhum modulo novo)
    cu = core.get(DL_.CUNHAGENS_REGISTRO) or {}; kh = core.get(DL_.KH_REGISTRO) or {}
    import guarda_frases_v411 as GF_
    V['cunhagens'], kh_ok_ = _ler_specs_v411(core, ESP, DL_, GF_, P)
    # cunhagens_v409 e kh_n1_cobertura_v409 (HERDADOS, RECRIADOS pelo rito da v411, por spec): cunhagens_v409 igual ao que a v410 SELOU (as 14 falas de 05/11 por sha256; as erratas e os extras intactos; errata nova, se houver, so' AO LADO, depois das seladas, assinada em nome proprio);
    # kh_n1_cobertura_v409 com as erratas IGUAIS as da v410 selada (a errata dos pisos da v411 mora no kh_n1_cobertura_v410); o veredito e' o esperado
    cu9_ = core.get('cunhagens_v409') or {}; kh9_ = core.get('kh_n1_cobertura_v409') or {}; cu9b_ = _base_core(PK).get('cunhagens_v409') or {}; kh9b_ = _base_core(PK).get('kh_n1_cobertura_v409') or {}
    e9_ = cu9_.get('erratas') or []; e9b_ = cu9b_.get('erratas') or []; k9e_ = kh9_.get('erratas') or []; k9eb_ = kh9b_.get('erratas') or []
    cu9_ok_ = bool(cu9_.get('all_verified') is True and cu9_.get('does_not_gate_core') is True and bool(cu9b_) and bool(cu9_.get('verbatim')) and _feq(cu9_.get('verbatim'), cu9b_.get('verbatim')) and len(cu9_.get('verbatim') or {}) == len(DL_.D9.VERBATIM_ORIGEM_V409) and all((v_ or {}).get('embedded_ok') is True for v_ in (cu9_.get('verbatim') or {}).values())
                   and _feq(cu9_.get('extras'), cu9b_.get('extras')) and len(e9_) >= len(e9b_) and _feq(e9_[:len(e9b_)], e9b_) and all(e_.get('assinatura') == DL_.ASSINA for e_ in e9_[len(e9b_):])
                   and bool(cu9_.get('checks')) and all(c_.get('ok') is True for c_ in cu9_.get('checks')) and cu9_.get('verdict') == _ev(ESP, 'cunhagens_v409') and not GUARDA.search(str(cu9_.get('verdict') or '')))
    kh9_ok_ = bool(kh9_.get('all_verified') is True and kh9_.get('does_not_gate_core') is True and bool(kh9b_) and bool(kh9_.get('checks')) and all(c_.get('ok') is True for c_ in kh9_.get('checks')) and bool(k9eb_) and len(k9e_) == len(k9eb_) and _feq(k9e_, k9eb_)
                   and kh9_.get('verdict') == _ev(ESP, 'kh_n1_cobertura_v409') and not GUARDA.search(str(kh9_.get('verdict') or '')))
    V['cunh410t'] = {'ok': cu9_ok_, 'verdict': cu9_.get('verdict'), 'n': len(cu9_.get('verbatim') or {}), 'n_erratas': len(e9_), 'n_erratas_novas': len(e9_) - len(e9b_), 'kh_ok': kh9_ok_, 'kh_verdict': kh9_.get('verdict')}
    if not cu9_ok_:
        P.append('cunhagens_v409 (HERDADA, recriada pelo rito) nao confere: as 14 falas de 05/11 (embedded_ok) e os extras iguais aos da v410 selada, as erratas seladas intactas (errata nova so\' ao lado, assinada em nome proprio), as checagens todas ok e o veredito esperado')
    if not kh9_ok_:
        P.append('kh_n1_cobertura_v409 (HERDADO, recriado pelo rito) nao confere: checagens (pisos h2 h3 h6, tamanho minimo h8) todas ok, as erratas IGUAIS as da v410 selada (a errata dos pisos, assinada na v411, esta em kh_n1_cobertura_v410), e o veredito esperado')
    # cunhagens_v408 e kh_n1_cobertura_v408 (HERDADOS, RECRIADOS pelo rito da v411, por spec): IGUAIS ao que a v410 SELOU (as 15 falas de 04/11 por sha256; as erratas E21 a E23, a E26 e a dos pisos, que ja' vinham da v410; os extras intactos); o veredito e' o esperado
    cu8_ = core.get('cunhagens_v408') or {}; kh8_ = core.get('kh_n1_cobertura_v408') or {}; cu8b_ = _base_core(PK).get('cunhagens_v408') or {}; kh8b_ = _base_core(PK).get('kh_n1_cobertura_v408') or {}
    e8_ = cu8_.get('erratas') or []; e8b_ = cu8b_.get('erratas') or []; k8e_ = kh8_.get('erratas') or []; k8eb_ = kh8b_.get('erratas') or []
    cu8_ok_ = bool(cu8_.get('all_verified') is True and cu8_.get('does_not_gate_core') is True and bool(cu8b_) and bool(cu8_.get('verbatim')) and _feq(cu8_.get('verbatim'), cu8b_.get('verbatim')) and len(cu8_.get('verbatim') or {}) == len(DL_.D8.VERBATIM_ORIGEM_V408) and all((v_ or {}).get('embedded_ok') is True for v_ in (cu8_.get('verbatim') or {}).values())
                   and _feq(cu8_.get('extras'), cu8b_.get('extras')) and bool(e8b_) and len(e8_) == len(e8b_) and _feq(e8_, e8b_)
                   and bool(cu8_.get('checks')) and all(c_.get('ok') is True for c_ in cu8_.get('checks')) and cu8_.get('verdict') == _ev(ESP, 'cunhagens_v408') and not GUARDA.search(str(cu8_.get('verdict') or '')))
    kh8_ok_ = bool(kh8_.get('all_verified') is True and kh8_.get('does_not_gate_core') is True and bool(kh8b_) and bool(kh8_.get('checks')) and all(c_.get('ok') is True for c_ in kh8_.get('checks')) and bool(k8eb_) and len(k8e_) == len(k8eb_) and _feq(k8e_, k8eb_)
                   and kh8_.get('verdict') == _ev(ESP, 'kh_n1_cobertura_v408') and not GUARDA.search(str(kh8_.get('verdict') or '')))
    V['cunh408d'] = {'ok': cu8_ok_, 'verdict': cu8_.get('verdict'), 'n': len(cu8_.get('verbatim') or {}), 'n_erratas': len(e8_), 'kh_ok': kh8_ok_, 'kh_verdict': kh8_.get('verdict')}
    if not cu8_ok_:
        P.append('cunhagens_v408 (HERDADA, recriada pelo rito) nao confere: as 15 falas de 04/11 (embedded_ok), os extras e as erratas IGUAIS aos da v410 selada (a E26 ao lado ja\' vinha dela), as checagens todas ok e o veredito esperado')
    if not kh8_ok_:
        P.append('kh_n1_cobertura_v408 (HERDADO, recriado pelo rito) nao confere: checagens todas ok, as erratas IGUAIS as da v410 selada (os pisos ja\' vinham dela), e o veredito esperado')
    # cunhagens_v407 e kh_n1_cobertura_v407 (HERDADOS, RECRIADOS): IGUAIS ao que a v410 SELOU (as 3 falas de 03/11; as erratas, inclusive a da D57(d) ao lado, que ja' vinha da v410); o veredito e' o esperado
    cu7_ = core.get('cunhagens_v407') or {}; kh7_ = core.get('kh_n1_cobertura_v407') or {}; cu7b_ = _base_core(PK).get('cunhagens_v407') or {}; kh7b_ = _base_core(PK).get('kh_n1_cobertura_v407') or {}
    e7_ = cu7_.get('erratas') or []; e7b_ = cu7b_.get('erratas') or []; k7e_ = kh7_.get('erratas') or []; k7eb_ = kh7b_.get('erratas') or []
    cu7_ok_ = bool(cu7_.get('all_verified') is True and cu7_.get('does_not_gate_core') is True and bool(cu7b_) and bool(cu7_.get('verbatim')) and _feq(cu7_.get('verbatim'), cu7b_.get('verbatim')) and len(cu7_.get('verbatim') or {}) == len(DL_.D7.VERBATIM_ORIGEM_V407) and all((v_ or {}).get('embedded_ok') is True for v_ in (cu7_.get('verbatim') or {}).values())
                   and _feq(cu7_.get('extras'), cu7b_.get('extras')) and bool(e7b_) and len(e7_) == len(e7b_) and _feq(e7_, e7b_)
                   and bool(cu7_.get('checks')) and all(c_.get('ok') is True for c_ in cu7_.get('checks')) and cu7_.get('verdict') == _ev(ESP, 'cunhagens_v407') and not GUARDA.search(str(cu7_.get('verdict') or '')))
    kh7_ok_ = bool(kh7_.get('all_verified') is True and kh7_.get('does_not_gate_core') is True and bool(kh7b_) and bool(kh7_.get('checks')) and all(c_.get('ok') is True for c_ in kh7_.get('checks')) and bool(k7eb_) and len(k7e_) == len(k7eb_) and _feq(k7e_, k7eb_)
                   and kh7_.get('verdict') == _ev(ESP, 'kh_n1_cobertura_v407') and not GUARDA.search(str(kh7_.get('verdict') or '')))
    V['cunh407d'] = {'ok': cu7_ok_, 'verdict': cu7_.get('verdict'), 'n': len(cu7_.get('verbatim') or {}), 'n_erratas': len(e7_), 'kh_ok': kh7_ok_, 'kh_verdict': kh7_.get('verdict')}
    if not cu7_ok_:
        P.append('cunhagens_v407 (HERDADA, recriada pelo rito) nao confere: as 3 falas de 03/11 (embedded_ok), os extras e as erratas IGUAIS aos da v410 selada (a da D57(d) ao lado ja\' vinha dela), as checagens todas ok e o veredito esperado')
    if not kh7_ok_:
        P.append('kh_n1_cobertura_v407 (HERDADO, recriado pelo rito) nao confere: checagens todas ok, as erratas IGUAIS as da v410 selada, e o veredito esperado')
    # cunhagens_v406 e kh_n1_cobertura_v406 (HERDADOS, RECRIADOS pelo rito da v411, por spec): IGUAIS ao que a v410 SELOU (as 23 falas de 02/11 por sha256, todas do operador; as erratas E14 a E17 e a E20 ao lado, que ja' vinham da v410; os pisos); o veredito NAO muda
    cu6_ = core.get('cunhagens_v406') or {}; kh6_ = core.get('kh_n1_cobertura_v406') or {}; cu6b_ = _base_core(PK).get('cunhagens_v406') or {}; kh6b_ = _base_core(PK).get('kh_n1_cobertura_v406') or {}
    e6_ = cu6_.get('erratas') or []; e6b_ = cu6b_.get('erratas') or []; k6e_ = kh6_.get('erratas') or []; k6eb_ = kh6b_.get('erratas') or []
    cu6_ok_ = bool(cu6_.get('all_verified') is True and cu6_.get('does_not_gate_core') is True and bool(cu6b_) and bool(cu6_.get('verbatim')) and _feq(cu6_.get('verbatim'), cu6b_.get('verbatim')) and len(cu6_.get('verbatim') or {}) == len(DL_.VERBATIM_ORIGEM_V406) and all((v_ or {}).get('embedded_ok') is True for v_ in (cu6_.get('verbatim') or {}).values())
                   and _feq(cu6_.get('extras'), cu6b_.get('extras')) and bool(e6b_) and len(e6_) == len(e6b_) and _feq(e6_, e6b_) and e6_[-1].get('agora') == DL_.ERRATA_E20 and str(e6_[-1].get('assinatura', '')).startswith('gerencia c1') and 'em nome proprio' in str(e6_[-1].get('assinatura', ''))
                   and bool(cu6_.get('checks')) and all(c_.get('ok') is True for c_ in cu6_.get('checks')) and cu6_.get('verdict') == _ev(ESP, 'cunhagens_v406') and not GUARDA.search(str(cu6_.get('verdict') or '')))
    kh6_ok_ = bool(kh6_.get('all_verified') is True and kh6_.get('does_not_gate_core') is True and bool(kh6b_) and bool(kh6_.get('checks')) and all(c_.get('ok') is True for c_ in kh6_.get('checks')) and bool(k6eb_) and len(k6e_) == len(k6eb_) and _feq(k6e_, k6eb_) and str(k6e_[-1].get('assinatura', '')).startswith('gerencia c1')
                   and kh6_.get('verdict') == _ev(ESP, 'kh_n1_cobertura_v406') and not GUARDA.search(str(kh6_.get('verdict') or '')))
    V['cunh406d'] = {'ok': cu6_ok_, 'verdict': cu6_.get('verdict'), 'n': len(cu6_.get('verbatim') or {}), 'n_erratas': len(e6_), 'kh_ok': kh6_ok_, 'kh_verdict': kh6_.get('verdict')}
    if not cu6_ok_:
        P.append('cunhagens_v406 (HERDADA, recriada pelo rito) nao confere: as 23 falas de 02/11 (embedded_ok), os extras e as erratas (E14 a E17 e a E20 ao lado, assinada em nome proprio) IGUAIS aos da v410 selada, as checagens (u7 versionada) todas ok e o veredito esperado')
    if not kh6_ok_:
        P.append('kh_n1_cobertura_v406 (HERDADO, recriado pelo rito) nao confere: checagens (pisos h2 h3 h6, tamanho minimo h8) todas ok, as erratas IGUAIS as da v410 selada (a dos pisos ao lado, assinada), e o veredito esperado')
    # os registros por spec da v410 (cunhagens_v404 e kh_n1_cobertura_v404, RECRIADOS): iguais aos selados
    c4_ = core.get('cunhagens_v404') or {}; k4_ = core.get('kh_n1_cobertura_v404') or {}; c4b_ = _base_core(PK).get('cunhagens_v404') or {}
    c4_ok_ = bool(c4_.get('all_verified') is True and c4_.get('does_not_gate_core') is True and bool(c4b_) and _feq(c4_.get('verbatim'), c4b_.get('verbatim')) and _feq(c4_.get('extras'), c4b_.get('extras')) and _feq(c4_.get('erratas'), c4b_.get('erratas')) and c4_.get('verdict') == (ESP.get('registros_v404') or {}).get('cunhagens_v404') and not GUARDA.search(str(c4_.get('verdict') or '')))
    k4_ok_ = bool(k4_.get('all_verified') is True and k4_.get('does_not_gate_core') is True and k4_.get('verdict') == (ESP.get('registros_v404') or {}).get('kh_n1_cobertura_v404'))
    V['cunh410b'] = {'n': len(c4_.get('verbatim') or {}), 'ok': c4_ok_, 'verdict': c4_.get('verdict'), 'kh_ok': k4_ok_}
    if not c4_ok_:
        P.append('cunhagens_v404 (recriada pelo rito) nao confere como a v410 a selou (selo, veredito, as falas, as erratas E7 a E9 e os extras)')
    if not k4_ok_:
        P.append('kh_n1_cobertura_v404 (recriada pelo rito) nao selou como a v410 a selou (selo, veredito, nao move o gate)')
    # cunhagens_v403 e kh_n1_cobertura_v403 (RECRIADOS pelo rito, por spec): iguais ao que a v410 SELOU (as DUAS falas de 27/10 embutidas por sha256, todas do operador; as erratas E5 e E6; as decisoes D17 a D22; os nomes; a leitura [ONTO] da tripla espectral)
    c3_ = core.get('cunhagens_v403') or {}; x3_ = c3_.get('extras') or {}; v3_ = c3_.get('verbatim') or {}; c3b_ = _base_core(PK).get('cunhagens_v403') or {}; aut3_ = x3_.get('autor_de_cada_inscricao') or {}
    c3_ok_ = bool(c3_.get('all_verified') is True and c3_.get('does_not_gate_core') is True and bool(c3b_) and bool(v3_) and _feq(v3_, c3b_.get('verbatim')) and all((v_ or {}).get('embedded_ok') is True for v_ in v3_.values()) and len(aut3_) == len(v3_) and all(a_ == 'operador' for a_ in aut3_.values())
                  and 'leitura_da_gerencia' not in x3_ and bool(c3_.get('checks')) and all(c_.get('ok') is True for c_ in c3_.get('checks')) and _feq(x3_, c3b_.get('extras')) and _feq(c3_.get('erratas'), c3b_.get('erratas')) and len(c3_.get('erratas') or []) == 2
                  and c3_.get('verdict') == (ESP.get('registros_v403') or {}).get('cunhagens_v403') and not GUARDA.search(str(c3_.get('verdict') or '')))
    k3_ = core.get('kh_n1_cobertura_v403') or {}
    k3_ok_ = bool(k3_.get('all_verified') is True and k3_.get('does_not_gate_core') is True and bool((ESP.get('registros_v403') or {}).get('kh_n1_cobertura_v403')) and k3_.get('verdict') == (ESP.get('registros_v403') or {}).get('kh_n1_cobertura_v403') and bool(k3_.get('checks')) and all(c_.get('ok') is True for c_ in k3_.get('checks')))
    V['cunh410'] = {'n': len(v3_), 'ok': c3_ok_, 'verdict': c3_.get('verdict'), 'n_erratas': len(c3_.get('erratas') or []), 'igual_ao_selado': bool(c3b_) and _feq(c3_, c3b_), 'kh_ok': k3_ok_}
    if not c3_ok_:
        P.append('cunhagens_v403 (recriada pelo rito): as duas falas de 27/10 (embedded_ok, todas do operador), as checagens, as erratas E5 e E6, as decisoes D17 a D22, os nomes e a leitura da tripla espectral nao conferem como a v410 as selou')
    if not k3_ok_:
        P.append('kh_n1_cobertura_v403 (recriada pelo rito) nao selou como a v410 a selou (selo, veredito, checagens, nao move o gate)')
    # cunhagens_v401 e kh_n1_cobertura_v401 (RECRIADOS pelo rito, por spec): iguais ao que a v410 SELOU (as seis inscricoes de 25/10 embutidas por sha256, todas do operador; as oito ratificacoes; a errata ao lado do adendo; a cadeia derivada [DERIVED] e a hipotese H_tau [OPEN])
    c1_ = core.get('cunhagens_v401') or {}; x1_ = c1_.get('extras') or {}; v1_ = c1_.get('verbatim') or {}; c1b_ = _base_core(PK).get('cunhagens_v401') or {}; aut1_ = x1_.get('autor_de_cada_inscricao') or {}
    c1_ok_ = bool(c1_.get('all_verified') is True and c1_.get('does_not_gate_core') is True and bool(c1b_) and bool(v1_) and _feq(v1_, c1b_.get('verbatim')) and all((v_ or {}).get('embedded_ok') is True for v_ in v1_.values()) and len(aut1_) == len(v1_) and all(a_ == 'operador' for a_ in aut1_.values())
                  and 'leitura_da_gerencia' not in x1_ and bool(c1_.get('checks')) and all(c_.get('ok') is True for c_ in c1_.get('checks')) and _feq(x1_, c1b_.get('extras')) and _feq(c1_.get('erratas'), c1b_.get('erratas')) and len(x1_.get('ratificacoes') or []) > 0
                  and c1_.get('verdict') == (ESP.get('registros_v401') or {}).get('cunhagens_v401') and not GUARDA.search(str(c1_.get('verdict') or '')))
    V['cunh401'] = {'n': len(v1_), 'ok': c1_ok_, 'verdict': c1_.get('verdict'), 'n_ratificacoes': len(x1_.get('ratificacoes') or []), 'igual_ao_selado': bool(c1b_) and _feq(c1_, c1b_)}
    if not c1_ok_:
        P.append('cunhagens_v401 (recriada pelo rito): as seis inscricoes de 25/10 (embedded_ok, todas do operador), as checagens, as oito ratificacoes, a errata do adendo, a cadeia derivada e a hipotese H_tau nao conferem como a v410 as selou')
    # cunhagens_v402 e kh_n1_cobertura_v402 (RECRIADOS pelo rito, por spec): iguais ao que a v410 SELOU (as TRES inscricoes de 26/10 embutidas por sha256, todas do operador; as quatro erratas E1 a E4; as decisoes D11 a D16; a leitura de 26/10 sobre a direcao do Um posto; a H_tau REFUTADA na forma literal)
    c2_ = core.get('cunhagens_v402') or {}; x2_ = c2_.get('extras') or {}; v2_ = c2_.get('verbatim') or {}; c2b_ = _base_core(PK).get('cunhagens_v402') or {}; aut2_ = x2_.get('autor_de_cada_inscricao') or {}
    c2_ok_ = bool(c2_.get('all_verified') is True and c2_.get('does_not_gate_core') is True and bool(c2b_) and bool(v2_) and _feq(v2_, c2b_.get('verbatim')) and all((v_ or {}).get('embedded_ok') is True for v_ in v2_.values()) and len(aut2_) == len(v2_) and all(a_ == 'operador' for a_ in aut2_.values())
                  and 'leitura_da_gerencia' not in x2_ and bool(c2_.get('checks')) and all(c_.get('ok') is True for c_ in c2_.get('checks')) and _feq(x2_, c2b_.get('extras')) and _feq(c2_.get('erratas'), c2b_.get('erratas')) and len(c2_.get('erratas') or []) == 4
                  and c2_.get('verdict') == (ESP.get('registros_v402') or {}).get('cunhagens_v402') and not GUARDA.search(str(c2_.get('verdict') or '')))
    k2_ = core.get('kh_n1_cobertura_v402') or {}
    k2_ok_ = bool(k2_.get('all_verified') is True and k2_.get('does_not_gate_core') is True and bool((ESP.get('registros_v402') or {}).get('kh_n1_cobertura_v402')) and k2_.get('verdict') == (ESP.get('registros_v402') or {}).get('kh_n1_cobertura_v402') and bool(k2_.get('checks')) and all(c_.get('ok') is True for c_ in k2_.get('checks')))
    V['cunh402'] = {'n': len(v2_), 'ok': c2_ok_, 'verdict': c2_.get('verdict'), 'n_erratas': len(c2_.get('erratas') or []), 'igual_ao_selado': bool(c2b_) and _feq(c2_, c2b_), 'kh_ok': k2_ok_}
    if not c2_ok_:
        P.append('cunhagens_v402 (recriada pelo rito): as tres inscricoes de 26/10 (embedded_ok, todas do operador), as checagens, as quatro erratas E1 a E4, as decisoes D11 a D16 e a leitura da direcao nao conferem como a v410 as selou')
    if not k2_ok_:
        P.append('kh_n1_cobertura_v402 (recriada pelo rito) nao selou como a v410 a selou (selo, veredito, checagens, nao move o gate)')
    # cunhagens_v399 (RECRIADA pelo rito): as QUATRO inscricoes de 24/10 por sha256, todas do operador, a declaracao e a direcao do testemunho, como a v399 as selou
    c9_ = core.get('cunhagens_v399') or {}; x9_ = c9_.get('extras') or {}; v9_ = c9_.get('verbatim') or {}; aut9_ = x9_.get('autor_de_cada_inscricao') or {}
    dx9_ = x9_.get('declaracao') or {}; dr9_ = x9_.get('direcao_do_testemunho') or {}
    c9_ok_ = bool(c9_.get('all_verified') is True and c9_.get('does_not_gate_core') is True and len(v9_) == 4 and all((v_ or {}).get('embedded_ok') is True for v_ in v9_.values()) and len(aut9_) == 4 and all(a_ == 'operador' for a_ in aut9_.values())
                  and bool(c9_.get('checks')) and all(c_.get('ok') is True for c_ in c9_.get('checks')) and dx9_.get('sha256') == EDC_.get('verbatim_sha256') and str(dx9_.get('estatuto')) == '[DECLARACAO DO OPERADOR / INPUT]'
                  and bool(edir_) and all(str(dr9_.get(k_) or '').startswith(v_) for k_, v_ in edir_.items()) and not _inv(json.dumps(x9_, ensure_ascii=False)))
    V['cunh399'] = {'n': len(v9_), 'ok': c9_ok_, 'verdict': c9_.get('verdict')}
    if not c9_ok_:
        P.append('cunhagens_v399 (recriada pelo rito): as quatro inscricoes de 24/10 (embedded_ok, todas do operador), as checagens, a declaracao e a direcao do testemunho nao conferem como a v399 as selou')
    cov = (core.get('kernel_formalization') or {}).get('axiom_coverage_v392') or {}   # o nome 'axiom_coverage_v392' e' do core (historico); segue na v411
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
