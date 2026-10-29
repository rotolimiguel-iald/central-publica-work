# -*- coding: utf-8 -*-
# [PREPARACAO v404, 28/10/2026 -- ESTADO] CONTEUDO v404 ESCRITO E TESTADO: derivado da v403 FINAL (a semente mecanica esta ao lado, em <arquivo>.bak_*_semente) e adaptado a mao ao conteudo da v404 (Jo 8,32, a projecao transversal da Meia-Nat, a errata de F2b ao lado, as nove falas de 28/10); testado pelo harness_textos_ensaio_v404.py e pelo harness_fechar_sandbox_v404.py.
# NAO e' versao selada: a gerencia revisa antes do rito. NAO rodar derivar_encanamento_v404.py --refazer sobre este arquivo (sobrescreveria a adaptacao a mao). Ver RELATORIO_PREPARACAO_v404.md.
# A LEITURA da rodada v404 (molde: leitura_v403.py, a que rodou em 28/10, que vem de leitura_v401.py e de leitura_v399.py FINAL, a de 24/10): SO LEITURA do Nos e da pasta da cadeia (work/cadeia_de_selo/v404, que aqui e' o proprio pacote).
# Devolve (V, PROBLEMAS); PROBLEMAS nao vazio => a cadeia PARA. Nenhum numero e' digitado: tudo sai dos JSON, do core, do selo, do sidecar e do stdout do rito; os vereditos e os valores esperados da rodada v404 sao LIDOS de ESPERADOS_v404.json.
# v404 (Jo 8,32 e a projecao transversal da Meia-Nat, as falas do operador de 28/10/2026): os registros NOVOS do core sao CINCO. TRES com FUNCAO, no runtime (lidos NA FRACTALIZACAO DO UM, logo depois das bandeiras_do_gate_v403): projecao_transversal_v404, jo8v32_v404 e f2b_errata_v404.
# Os dois primeiros leem do kernel do proprio rito a composicao, a estrela, o contrato e o suporte da sua pedra (TGLExt.ProjecaoTransversalDaMeiaNat, TGLExt.Jo8v32) e CALCULAM um modelo honesto com beta = alfa x raiz de e em runtime; o terceiro (a errata de F2b) NAO tem pedra: le o V1 do ramo B por hash,
# a calibracao A e a previsao do par, e confere que o canal passou de AWAITING a retirado antes do dado SEM reescrever o V1, o livro v383 nem o registro da v386 (a errata e' AO LADO). DOIS por spec: cunhagens_v404 (as NOVE falas do operador de 28/10 por sha256, as erratas E7 a E9 e as decisoes D23 a D26
# em nome proprio da gerencia c1, a leitura da massa) e kh_n1_cobertura_v404 (a cobertura exata do Audit). Os SEIS registros da v403 (caminho_v403, vida_v403, verdade_adendo_v403, bandeiras_do_gate_v403, cunhagens_v403, kh_n1_cobertura_v403), os CINCO da v402, os TRES da v401 e os QUATRO da v399 sao RECRIADOS
# pelo rito no mesmo ponto do main e tem de seguir selados e iguais ao ensaio a seco (e a v403 selada: base_v403); os da v398 (sonico, afinacao, cunhagens, kh), da v397, da v396, da v395, da v394 e da v393 seguem selados.
# Os DOIS modulos novos de kernel vem de ESPERADOS[pedras_sha256] e sao conferidos aqui contra os arquivos do kernel do Nos (sha256); as TRES pedras SELADAS da v403 (Caminho, Vida, VerdadeAdendo) seguem no kernel com o sha de ESPERADOS[pedras_v403_sha256] (registro: pedra selada nao se renomeia por cima);
# a composicao, a estrela, o contrato e o suporte de cada pedra nova vem de ESPERADOS[teoremas_das_pedras, bandeiras_das_pedras, estrelas_v404, contrato_das_pedras, suporte_das_pedras] e o calculo de cada registro, de ESPERADOS[registros_funcao_v404] (projecao, jo8v32 e f2b).
# A escada vem de ESPERADOS[escada_v403_e_v404] e ESPERADOS[escada]; a troca dita (so numeros) e' a de ESPERADOS[troca_dita]. O GATE NAO SE MOVE: o qg_closure do core e' IDENTICO ao da v403 (os sete checks, a letra do veredito, as 18 bandeiras: ESPERADOS[qg_closure_gate_verdict_v403, qg_closure_v403_checks]);
# a funcao do neutrino NAO e' reescrita (o angle_status antigo fica) e o V1 do ramo B (v386) segue AWAITING_DATA: a errata de F2b e' AO LADO.
# O SIDECAR um_absoluto_selo_acom.json (arquivo da custodia desde a v399, REESCRITO pelo rito) e' lido aqui: existe, e' JSON valido, o veredito e' ALL_OBJECTS_SEALED, tem os tres objetos (um.py, core e selo) com o SHA-256 igual ao dos arquivos do Nos, sem recusas, com a secao de honestidade (confidencialidade NAO alegada).
# A DIRECAO DO TESTEMUNHO (v399) segue conferida nos registros recriados: o operador testifica DA IALD; o um.py testifica EM HASH; a IALD NAO testifica do operador. As NOVE falas de 28/10 sao TODAS falas do operador (nenhuma e' da gerencia); as erratas E7 a E9 e as decisoes D23 a D26 sao da gerencia c1, em nome proprio, assinadas no registro.
# O QUADRO «O Teste da Unica Palavra» (v397) segue selado e igual: o registro teste_de_veracidade_fase9_v397 == ESPERADOS e == o resultado pinado, o quadro sela nas duas linguas, e a conferencia do rito diz que ele segue no topo (artigo PT/EN e .md).
# A face de Fock do psion segue CONDICIONAL (psibit_v395 e testemunha_estatica_v396); as linhas `[v399]`, `[v398]` e `[v397]` do stdout do rito (as etiquetas que o programa imprime), a `[v401]`, a `[v402]` e a `[v403]` (recriadas) e a nova `[v404]` dizem os vereditos e registros por spec selados == registros por spec;
# o AVISO de qualquer bloco v393 a v404 no stdout reprova, e a linha de RECUSA do registro f2b_errata_v404 ou do bandeiras_do_gate_v403 tambem.
# A linha final do rito: o main imprime, por ultimo, a linha do sidecar (`[selo_acom] ... ALL_OBJECTS_SEALED ; objetos 3 ; recusas 0`), logo depois da do colapso tipado; a leitura exige as DUAS, nessa ordem.
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CONTRATO COM textos_v404.py (as CHAVES NOVAS ou MUDADAS de V na v404; as demais sao as da v403, com o mesmo significado):
#   V['projecao'], V['jo8v32']                 cada um {'verdict','ok'(all_verified),'n_checks','mech_ok','values','values_ok'(== ESPERADOS[registros_funcao_v404][k]['values']),'beta_ok','kernel_ok'(composicao, contrato e suporte no kernel do rito e no trio),'estrela_ok','contexto_ok','unconditional_ok','key_ok',
#                                                  'flag'(ESPERADOS[bandeiras_das_pedras][k]),'flag_true','theorem'(ESPERADOS[teoremas_das_pedras][k]),'estrela'(teorema, bandeira),'registro'(nome),'runtime_executed','does_not_gate_core','sealed'(a conjuncao de tudo: o registro selou inteiro)}
#   V['f2b']                                   o registro f2b_errata_v404 (SEM pedra) {'registro','verdict','ok','sealed','n_checks','mech_ok','values','values_ok','beta_ok','ao_lado_ok'(o V1, o registro da v386 e a cobranca F2b da v386 como antes; o canal agora retirado antes do dado),'neutrino_intacto',
#                                                  'status_antes','status_agora','runtime_executed','does_not_gate_core'}
#   V['gate']                                  o registro bandeiras_do_gate_v403 RECRIADO (F8.1 da v403) {'registro','verdict','ok','sealed','n_checks','mech_ok','values','values_ok','f81_ok','n18','n_ls2','n_checks_do_gate','sonda','runtime_executed','does_not_gate_core'}; V['f81_conf'] = o que a conferencia do rito diz da F8.1 (releitura_ok, gate_igual)
#   V['fun402'], V['fun403']                   {'ponte':{...},'queda':{...},'esperanca':{...}} (v402) e {'caminho':{...},'vida':{...},'verdade_adendo':{...}} (v403): os registros com funcao RECRIADOS {'registro','verdict','ok','sealed','n_checks','mech_ok'(== a v403 selada),'values_ok'(== a v403 selada),'beta_ok','kernel_ok'}; V['pedras_v403'] = {rel: {'sha16','ok'}} (as TRES pedras seladas da v403 no kernel)
#   V['fal401']                                {'verdict','ok','sealed','n_checks','mech_ok','values_ok'(== a v403 selada),'beta_ok','chain_ok','kernel_ok','costless_ok','runtime_executed','does_not_gate_core'} (a falsidade da v401, RECRIADA); o veredito == ESPERADOS[veredito_da_falsidade_v403]
#   V['reg401'], V['reg402'], V['reg403']      LISTAS dos nomes da v401 (3), da v402 (5) e da v403 (6) recriados; V['reg401_estado'], V['reg402_estado'], V['reg403_estado'] = {nome: {'verdict','ok'}}
#   V['reg404']                                DICT nome -> {'verdict','ok'} dos 5 registros NOVOS (os 3 com funcao + cunhagens_v404 + kh_n1_cobertura_v404); V['registros_novos'] = esses 5 nomes (sorted); V['reg_todos'] os exigidos
#   V['pedras']                                LISTA de 2 dicts {'key'(projecao|jo8v32),'modulo'('TGLExt.ProjecaoTransversalDaMeiaNat' ...),'rel','sha16','sha256','bytes','bandeiras'(ESPERADOS[pedras][rel]['bandeiras']),'decl'(None),'ok'}; V['n_pedras'] = 2
#   V['pedras_kernel']                         {'projecao':{...},'jo8v32':{...}} cada um {'rel','flag','flag_true','theorem','axioms','source','contrato_ok','suporte_ok','estrela_ok','kernel_ok','n_contrato','n_suporte','estrela'}
#   V['cunhagens']                             (cunhagens_v404) {'ok','verdict','n'(9),'verbatim_ok','todas_do_operador','autores','erratas_ok','n_erratas'(3),'decisoes_ok','n_decisoes','nomes_ok','massa_ok','reg403_ok','teoremas_ok','n_checks','checks_ok','kernel_ok','kh_ok'}; V['verbatins'] = as 9 falas {chave: {'sha16','bytes'}}
#   V['cunh403'] (cunhagens_v403 recriada) {'ok','verdict','n'(2),'n_erratas'(2),'igual_ao_selado','kh_ok'}; V['cunh402'] (cunhagens_v402 recriada) {'ok','verdict','n'(3),'n_erratas'(4),'igual_ao_selado','kh_ok'}; V['cunh401'] (cunhagens_v401 recriada) {'ok','verdict','n','n_ratificacoes','igual_ao_selado'}; V['cunh399'] (a recriada da v399, como antes)
#   V['kh']                                    {'decl','thm','fora','nao_lidas','verdict'(kh_n1_cobertura_v404)}; V['cunh_verdict'] = o veredito de cunhagens_v404
#   V['h8']                                    o numero de entradas do hash formal do rito (== ESPERADOS[h8_entradas]); V['n_bandeiras'] e V['n_bandeiras_por_pedra'] (do registro cunhagens_v404 == ESPERADOS)
# (a linha de stdout [v404] a conferir: `[v404] a projecao transversal, o jo8v32 e a errata de F2b (a projecao e o jo8v32 lidos depois das bandeiras do gate; a errata de F2b depois da errata ao lado de R6 da v386) e as falas de 28/10 (cunhagens_v404): projecao=... | jo8v32=... | f2b=... | cunhagens=... | registros por spec: N (selados N)`)
import glob, hashlib, json, os, re, sys, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
PK = os.path.dirname(HERE)            # work\cadeia_de_selo\v404
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
FINAL_RE = re.compile(r'^\[selo\] colapso tipado: ')
TRAILER_RE = re.compile(r'^(exit=\d+|rc=\d+|RITO_RC=\S+|inicio |fim )')
GUARDA = re.compile('(?<!NOT_)(?<!UN)' + 'CONF' + 'IRMED|(?<!AP)PRO' + 'VED_BY|TGL_PRO' + 'VED')
REG_V393 = ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393", "kh_n1_cobertura_v393")   # da v393: seguem no core e seguem selados (nao sao 'novos' da v404)
REG_V394 = ("tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394", "criterio_binario_de_parada_v394")   # da v394: seguem no core e seguem selados (nao sao 'novos' da v404)
REG_V395 = ("psibit_v395", "cunhagens_v395", "kh_n1_cobertura_v395")   # da v395: seguem no core e seguem selados (nao sao 'novos' da v404)
REG_V396 = ("testemunha_estatica_v396", "cunhagens_v396", "kh_n1_cobertura_v396")   # da v396: seguem no core e seguem selados (nao sao 'novos' da v404)
REG_V397 = ("teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397")   # da v397 (o Teste da Unica Palavra, a pedra Token e as falas de 23/10): seguem no core e seguem selados; o quadro do topo le o primeiro
REG_V398 = ("sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398")   # da v398 (o sonico, a afinacao das cordas e as falas de 23/10): seguem no core e seguem selados (nao sao 'novos' da v404)
REG_V401 = ("falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401")   # os TRES registros da v401: RECRIADOS pelo rito da v404 (o primeiro com FUNCAO), tem de seguir selados e iguais ao ensaio a seco (e a v403 selada)
REG_V402 = ("ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "cunhagens_v402", "kh_n1_cobertura_v402")   # os CINCO registros da v402 (tres com FUNCAO, dois por spec): RECRIADOS pelo rito da v404, tem de seguir selados e iguais ao ensaio a seco (e a v403 selada)
REG_V403 = ("caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "cunhagens_v403", "kh_n1_cobertura_v403")   # os SEIS registros da v403 (quatro com FUNCAO, dois por spec): RECRIADOS pelo rito da v404, tem de seguir selados e iguais ao ensaio a seco (e a v403 selada)
REG_V399 = ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399")   # os QUATRO registros da v399: RECRIADOS pelo rito da v404 (os dois primeiros com FUNCAO), tem de seguir selados e iguais ao ensaio a seco
FUN_V402 = {"ponte": "ponte_da_escala_dual_v402", "queda": "queda_sem_geometria_v402", "esperanca": "esperanca_condicional_v402"}   # os TRES registros com FUNCAO da v402 (recriados)
FUN_V403 = {"caminho": "caminho_v403", "vida": "vida_v403", "verdade_adendo": "verdade_adendo_v403"}   # os TRES registros com FUNCAO das pedras da v403 (recriados); o quarto, bandeiras_do_gate_v403, e' lido a parte (V['gate'])
REG_FUNCAO = ("projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404")   # os TRES registros NOVOS com FUNCAO (no runtime; o ultimo, a errata de F2b, nao tem pedra)
REG_FIXOS = REG_FUNCAO + ("cunhagens_v404", "kh_n1_cobertura_v404")   # os CINCO registros NOVOS do core v404 (tres com FUNCAO, dois por spec); + os de ESPERADOS[registros_v404] (REG_TODOS, dentro de ler)
PEDRA_DE = {"projecao": "projecao_transversal_v404", "jo8v32": "jo8v32_v404"}   # chave da pedra -> registro com funcao que a le (conferido contra delta_v404.REGISTRO_DE_PEDRA dentro de ler)
SIDECAR_RE = re.compile(r'^\[selo_acom\] (TGL_SELO_ACOM_SIDECAR_V399__ALL_OBJECTS_SEALED\S*) ; objetos (\d+) ; recusas (\d+)$')   # a linha que o main da v404 imprime por ultimo (selo_acom_sidecar_v399)
_RX_INV = re.compile(r'IALD\s+testifica\s+(?:a\s+mim|do\s+operador|de\s+mim)')   # a DIRECAO invertida (a IALD como quem testifica DO operador); so' a fala em que ele a recusa escapa
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()


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


_BASE_CORE = {}


def _base_core(pk):
    """O core da v403 SELADA (copia de bytes em PK/base_v403): de onde saem o teorema e o modulo da face de Fock da testemunha (nenhum nome digitado); lido uma vez por caminho."""
    p = os.path.join(pk, 'base_v403', 'um_absoluto.json')
    if p not in _BASE_CORE:
        _BASE_CORE[p] = json.load(open(p, encoding='utf-8'))['core']
    return _BASE_CORE[p]


def _res_path(ev):
    """O resultado pinado do Teste da Unica Palavra: a copia em PK/insumos/fase9 (so' existe no SANDBOX do harness) ou, no real, a copia duravel da v397 (ESPERADOS[veracidade][resultado][duravel]); o sha256 e' conferido contra ESPERADOS em ambos."""
    nome = os.path.basename((ev.get('resultado') or {}).get('duravel') or 'ausente')
    loc = os.path.join(PK, 'insumos', 'fase9', nome)
    return loc if os.path.exists(loc) else ((ev.get('resultado') or {}).get('duravel') or loc)
def ler():
    P = []
    ESP = json.load(open(os.path.join(PK, 'ESPERADOS_v404.json'), encoding='utf-8')); CM = json.load(open(os.path.join(PK, 'CANDIDATO_v404.json'), encoding='utf-8'))
    ap, app = _aplicado()
    REG_TODOS = tuple(dict.fromkeys(tuple(REG_FIXOS) + tuple(ESP.get('registros_v404') or ())))
    core = json.load(open(os.path.join(NOS, 'um_absoluto.json'), encoding='utf-8'))['core']; selo = json.load(open(os.path.join(NOS, 'um_absoluto_selo.json'), encoding='utf-8'))
    stp = os.path.join(NOS, 'rodada_v404_stdout.txt'); out = open(stp, encoding='utf-8', errors='replace').read() if os.path.exists(stp) else ''
    V = {'nos': NOS, 'aplicado_json': app, 'pk': PK}
    if not out:
        P.append('rodada_v404_stdout.txt ausente ou vazio')
    V['s64'] = sha(os.path.join(NOS, 'um.py')); V['s16'] = V['s64'][:16]; V['umb'] = os.path.getsize(os.path.join(NOS, 'um.py'))
    if str((selo.get('sha256') or {}).get('um.py', '')) != V['s64']:
        P.append('selo.sha256(um.py) != disco')
    if not (ap['um_py_novo']['sha16'] == V['s16'] == ESP['candidato_sha16'] == CM['sha16']):
        P.append('um.py do disco != instalado/esperado/candidato')
    V['base16'] = ap['backups']['um.py']['sha16']; V['base_backup'] = ap['backups']['um.py']['backup']
    if V['base16'] != ESP['origem_sha16']:
        P.append('a base substituida != a v403 selada')
    V['n_patches'] = len(CM['patches']); V['patches'] = ', '.join(p['id'] for p in CM['patches']); V['patch_ids'] = [p['id'] for p in CM['patches']]
    V['instalado_em'] = '%s-%s-%s %s:%s:%s' % (ap['ts'][0:4], ap['ts'][4:6], ap['ts'][6:8], ap['ts'][9:11], ap['ts'][11:13], ap['ts'][13:15])
    m = re.search(r'teoremas limpos:\s*(\d+)/(\d+)', out); V['teor'] = '%s/%s' % m.groups() if m else 'AUSENTE'
    V['escada_antes'] = ESP['escada_v403_e_v404'][0]; V['escada_depois'] = ESP['escada'][1]
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
    avisos_ = [l.strip()[:200] for l in out.splitlines() if '[v404] AVISO' in l or '[v403] AVISO' in l or '[v402] AVISO' in l or '[v401] AVISO' in l or '[v399] AVISO' in l or '[selo_acom] AVISO' in l]
    if avisos_:
        P.append('o stdout traz AVISO da v404 (a projecao transversal, o jo8v32, a errata de F2b, os registros por spec, os registros recriados da v403, da v402, da v401 ou da v399, o selo ACOM, a declaracao do operador ou o sidecar nao rodaram): %s' % avisos_[:2])
    elif [l for l in out.splitlines() if re.search(r'\[v39[3-8]\] AVISO', l)]:
        P.append('o stdout traz AVISO de um bloco anterior (v393 a v398): %s' % [l.strip()[:200] for l in out.splitlines() if re.search(r'\[v39[3-8]\] AVISO', l)][:2])
    if [l for l in out.splitlines() if '[v403] RECUSA' in l]:
        P.append('o stdout traz a RECUSA do registro bandeiras_do_gate_v403 (uma bandeira CALCULADA do gate veio False ou uma checagem do registro falhou: fail-closed): %s' % [l.strip()[:200] for l in out.splitlines() if '[v403] RECUSA' in l][:1])
    if [l for l in out.splitlines() if '[v404] RECUSA' in l]:
        P.append('o stdout traz a RECUSA do registro f2b_errata_v404 (uma checagem da errata de F2b falhou: o canal fica como antes e o rito para; fail-closed): %s' % [l.strip()[:200] for l in out.splitlines() if '[v404] RECUSA' in l][:1])
    RF_ = ESP.get('registros_funcao_v404') or {}   # projecao|jo8v32|f2b -> {nome, verdict, values, n_checks} do ensaio a seco
    RF3_ = ESP.get('registros_funcao_v403') or {}   # caminho|vida|verdade_adendo|gate -> o mesmo, dos registros da v403 (recriados pelo rito da v404)
    EV2_ = ESP.get('vereditos_v403') or {}   # os vereditos da v403 SELADA (os registros da v403 sao recriados e tem de dar os mesmos)
    for r_, e_ in (('selo_pela_propria_tecnologia_v399', (ESP.get('selo_acom') or {}).get('verdict')), ('declaracao_do_operador_v399', (ESP.get('declaracao') or {}).get('verdict')), ('falsidade_da_inercia_v401', ESP.get('veredito_da_falsidade_v403')),
                   ('ponte_da_escala_dual_v402', EV2_.get('ponte_da_escala_dual_v402')), ('queda_sem_geometria_v402', EV2_.get('queda_sem_geometria_v402')), ('esperanca_condicional_v402', EV2_.get('esperanca_condicional_v402')),
                   ('caminho_v403', (RF3_.get('caminho') or {}).get('verdict')), ('vida_v403', (RF3_.get('vida') or {}).get('verdict')), ('verdade_adendo_v403', (RF3_.get('verdade_adendo') or {}).get('verdict')), ('bandeiras_do_gate_v403', (RF3_.get('gate') or {}).get('verdict')),
                   ('projecao_transversal_v404', (RF_.get('projecao') or {}).get('verdict')), ('jo8v32_v404', (RF_.get('jo8v32') or {}).get('verdict')), ('f2b_errata_v404', (RF_.get('f2b') or {}).get('verdict'))):
        if not e_ or ('>>> %s <<<' % e_) not in out:
            P.append('o bloco %s do stdout nao traz a linha `>>> veredito <<<` do ensaio a seco' % r_)
    m_s9 = re.search(r'\[v399\] o selo pela propria tecnologia e a declaracao do operador \(lidos depois da afinacao das cordas\) e as inscricoes de 24/10 \(cunhagens_v399\): selo=(\S+) \| declaracao=(\S+) \| cunhagens=(\S+) \| registros por spec: (\d+) \(selados (\d+)\)', out)
    if (not m_s9 or (m_s9.group(1), m_s9.group(2), m_s9.group(3)) != ((ESP.get('selo_acom') or {}).get('verdict'), (ESP.get('declaracao') or {}).get('verdict'), (ESP.get('registros_v399') or {}).get('cunhagens_v399'))
            or m_s9.group(4) != m_s9.group(5) or int(m_s9.group(4)) != len(ESP.get('registros_v399') or {})):
        P.append('a linha [v399] do stdout (selo, declaracao e cunhagens_v399; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(ESP.get('registros_v399') or {}), m_s9.groups()[3:] if m_s9 else 'ausente'))
    m_s1 = re.search(r'\[v401\] a falsidade \(simulacro\) da inercia \(lida depois da declaracao do operador\) e as inscricoes de 25/10 \(cunhagens_v401\): falsidade=(\S+) \| cunhagens=(\S+) \| registros por spec: (\d+) \(selados (\d+)\)', out)
    if (not m_s1 or (m_s1.group(1), m_s1.group(2)) != (ESP.get('veredito_da_falsidade_v403'), (ESP.get('registros_v401') or {}).get('cunhagens_v401')) or m_s1.group(3) != m_s1.group(4) or int(m_s1.group(3)) != len(ESP.get('registros_v401') or {})):
        P.append('a linha [v401] do stdout (falsidade e cunhagens_v401, recriados; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(ESP.get('registros_v401') or {}), m_s1.groups()[2:] if m_s1 else 'ausente'))
    m_s2 = re.search(r'\[v402\] a ponte, a queda e a esperanca \(lidas depois da falsidade da inercia\) e as inscricoes de 26/10 \(cunhagens_v402\): ponte=(\S+) \| queda=(\S+) \| esperanca=(\S+) \| cunhagens=(\S+) \| registros por spec: (\d+) \(selados (\d+)\)', out)
    if (not m_s2 or (m_s2.group(1), m_s2.group(2), m_s2.group(3), m_s2.group(4)) != (EV2_.get('ponte_da_escala_dual_v402'), EV2_.get('queda_sem_geometria_v402'), EV2_.get('esperanca_condicional_v402'), (ESP.get('registros_v402') or {}).get('cunhagens_v402'))
            or m_s2.group(5) != m_s2.group(6) or int(m_s2.group(5)) != len(ESP.get('registros_v402') or {})):
        P.append('a linha [v402] do stdout (ponte, queda, esperanca e cunhagens_v402, recriados; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(ESP.get('registros_v402') or {}), m_s2.groups()[4:] if m_s2 else 'ausente'))
    m_s3 = re.search(r'\[v403\] o caminho, a vida, o adendo da verdade e as bandeiras do gate \(lidos depois da esperanca condicional\) e as falas de 27/10 \(cunhagens_v403\): caminho=(\S+) \| vida=(\S+) \| verdade_adendo=(\S+) \| bandeiras=(\S+) \| cunhagens=(\S+) \| registros por spec: (\d+) \(selados (\d+)\)', out)
    if (not m_s3 or tuple(m_s3.group(i_) for i_ in range(1, 6)) != ((RF3_.get('caminho') or {}).get('verdict'), (RF3_.get('vida') or {}).get('verdict'), (RF3_.get('verdade_adendo') or {}).get('verdict'), (RF3_.get('gate') or {}).get('verdict'), (ESP.get('registros_v403') or {}).get('cunhagens_v403'))
            or m_s3.group(6) != m_s3.group(7) or int(m_s3.group(6)) != len(ESP.get('registros_v403') or {})):
        P.append('a linha [v403] do stdout (caminho, vida, verdade_adendo, bandeiras e cunhagens_v403, recriados; registros por spec selados == %d) esta ausente ou difere da v403 selada (%s)' % (len(ESP.get('registros_v403') or {}), m_s3.groups()[5:] if m_s3 else 'ausente'))
    m_s4 = re.search(r'\[v404\] a projecao transversal, o jo8v32 e a errata de F2b \(a projecao e o jo8v32 lidos depois das bandeiras do gate; a errata de F2b depois da errata ao lado de R6 da v386\) e as falas de 28/10 \(cunhagens_v404\): projecao=(\S+) \| jo8v32=(\S+) \| f2b=(\S+) \| cunhagens=(\S+) \| registros por spec: (\d+) \(selados (\d+)\)', out)
    if (not m_s4 or tuple(m_s4.group(i_) for i_ in range(1, 5)) != ((RF_.get('projecao') or {}).get('verdict'), (RF_.get('jo8v32') or {}).get('verdict'), (RF_.get('f2b') or {}).get('verdict'), (ESP.get('registros_v404') or {}).get('cunhagens_v404'))
            or m_s4.group(5) != m_s4.group(6) or int(m_s4.group(5)) != len(ESP.get('registros_v404') or {})):
        P.append('a linha [v404] do stdout (projecao, jo8v32, f2b e cunhagens_v404; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(ESP.get('registros_v404') or {}), m_s4.groups()[4:] if m_s4 else 'ausente'))
    # a linha [v398] que o main da v404 segue imprimindo (o sonico, a afinacao das cordas e as cunhagens da v398): igual ao que a v403 selou
    ev8_ = ESP.get('vereditos_v403') or {}
    n_spec8_ = len([k_ for k_ in REG_V398 if k_ not in ('sonico_v398', 'afinacao_das_cordas_v398')])
    m_s8 = re.search(r'\[v398\] o sonico e a afinacao das cordas \(lidos na fractalizacao do Um\) e as inscricoes de 23/10 \(cunhagens_v398\): sonico=(\S+) \| afinacao=(\S+) \| cunhagens=(\S+) \| registros por spec: (\d+) \(selados (\d+)\)', out)
    if (not m_s8 or (m_s8.group(1), m_s8.group(2), m_s8.group(3)) != (ev8_.get('sonico_v398'), ev8_.get('afinacao_das_cordas_v398'), ev8_.get('cunhagens_v398')) or m_s8.group(4) != m_s8.group(5) or int(m_s8.group(4)) != n_spec8_):
        P.append('a linha [v398] do stdout (sonico, afinacao e cunhagens_v398; registros por spec selados == %d) esta ausente ou difere da que a v403 selou (%s)' % (n_spec8_, m_s8.groups()[3:] if m_s8 else 'ausente'))
    # as duas linhas [v397] que o main da v404 segue imprimindo (o Teste da Unica Palavra e as cunhagens da v397): iguais ao que a v397 selou
    m_tv = re.search(r'\[v397\] o Teste da Unica Palavra \(Fase 9 V2-c1, aberto uma vez em 23/10\), lido por hash ao lado do V1 \(nenhum sigma novo\): (\S+)', out)
    if not m_tv or m_tv.group(1) != ev8_.get('teste_de_veracidade_fase9_v397'):
        P.append('a linha [v397] do Teste da Unica Palavra esta ausente do stdout ou difere da que a v397 selou (%s)' % (m_tv.group(1)[:80] if m_tv else 'ausente'))
    n_spec7_ = len([k_ for k_ in REG_V397 if k_ != 'teste_de_veracidade_fase9_v397'])
    m_sp = re.search(r'\[v397\] a pedra Token e as falas de 23/10 \(cunhagens_v397\): (\S+) \| registros por spec: (\d+) \(selados (\d+)\)', out)
    if not m_sp or m_sp.group(1) != ev8_.get('cunhagens_v397') or m_sp.group(2) != m_sp.group(3) or int(m_sp.group(2)) != n_spec7_:
        P.append('a linha [v397] das cunhagens da v397 esta ausente do stdout ou difere da que a v397 selou (registros por spec selados == %d)' % n_spec7_)
    hp = os.path.join(PK, 'rito_horarios_v404.txt'); V['horarios'] = open(hp, encoding='utf-8').read().split() if os.path.exists(hp) else []
    V['selo_ts'] = selo.get('timestamp'); V['um_version'] = selo.get('um_version'); V['qg'] = selo.get('qg_closure_verdict')
    if V['um_version'] != 'v404':
        P.append('o selo nao e v404')
    if V['qg'] != ESP['qg_closure_verdict']:
        P.append('o gate MUDOU')
    qg = core.get('qg_closure') or {}
    V['n18'] = sum(1 for fam in ('formal_flags', 'physics_flags', 'experiment_flags') for v in (qg.get(fam) or {}).values() if v is True)
    if V['n18'] != 18:
        P.append('as bandeiras do gate nao sao 18 True (%s)' % V['n18'])
    for k in ('um_absoluto.json', 'um_absoluto_selo.json', 'um_absoluto_selo_acom.json', 'um_absoluto_forma_canonica.md', 'um_absoluto_manifest.md'):
        V['h_' + k] = sha(os.path.join(NOS, k))[:16] if os.path.exists(os.path.join(NOS, k)) else 'AUSENTE'
    V['artigos'] = {os.path.basename(p): sha(p)[:16] for p in sorted(glob.glob(os.path.join(NOS, 'um_absoluto_??.pdf')) + glob.glob(os.path.join(NOS, 'um_absoluto_??.txt')))}
    cp = os.path.join(HERE, 'conferidor', 'conferencia_rito_v404.json')
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
        if C.get('veredito_falsidade') != ESP.get('veredito_da_falsidade_v403'):
            P.append('a conferencia do rito traz o veredito da falsidade (falsidade_da_inercia_v401) diferente do ensaio a seco')
        for chv_, esp_v_, nome_ in (('veredito_ponte', EV2_.get('ponte_da_escala_dual_v402'), 'ponte_da_escala_dual_v402'), ('veredito_queda', EV2_.get('queda_sem_geometria_v402'), 'queda_sem_geometria_v402'), ('veredito_esperanca', EV2_.get('esperanca_condicional_v402'), 'esperanca_condicional_v402'),
                                    ('veredito_caminho', (RF3_.get('caminho') or {}).get('verdict'), 'caminho_v403'), ('veredito_vida', (RF3_.get('vida') or {}).get('verdict'), 'vida_v403'), ('veredito_verdade_adendo', (RF3_.get('verdade_adendo') or {}).get('verdict'), 'verdade_adendo_v403'),
                                    ('veredito_bandeiras_do_gate', (RF3_.get('gate') or {}).get('verdict'), 'bandeiras_do_gate_v403'),
                                    ('veredito_projecao', (RF_.get('projecao') or {}).get('verdict'), 'projecao_transversal_v404'), ('veredito_jo8v32', (RF_.get('jo8v32') or {}).get('verdict'), 'jo8v32_v404'), ('veredito_f2b', (RF_.get('f2b') or {}).get('verdict'), 'f2b_errata_v404')):
            if not C.get(chv_) or C.get(chv_) != esp_v_:
                P.append('a conferencia do rito traz o veredito de %s (%s) ausente ou diferente do ensaio a seco' % (nome_, chv_))
        f81c_ = C.get('f81') or {}
        V['f81_conf'] = {'releitura_ok': f81c_.get('releitura_ok'), 'gate_igual': f81c_.get('gate_igual'), 'ls2': len(f81c_.get('ls2') or []), 'sonda': len(f81c_.get('sonda') or []), 'qg_checks_n': f81c_.get('qg_checks_n')}
        if not (f81c_.get('releitura_ok') is True and f81c_.get('gate_igual') is True):
            P.append('a conferencia do rito diz que a releitura da F8.1 (as tres bandeiras antes literais calculadas no um.py instalado, as fontes delas, o qg_closure sem a lista de checks e a letra do veredito do gate) NAO conferiu')
        if C.get('marcador_ficou'):
            P.append('o marcador .servidor_parado_pelo_rito ficou: o servidor do modelo pode estar parado')
    else:
        V['conf16'] = 'AUSENTE'; P.append('a conferencia do rito nao foi achada em pos_rito/conferidor')
    V['troca_dita'] = list(ESP['troca_dita'])
    V['n_ver'] = len(ESP['vereditos_v403'])
    # --- os registros novos: descobertos por comparacao com o que a v403 ja tinha
    novos = []
    for k, r in core.items():
        if isinstance(r, dict) and 'verdict' in r and k not in ESP['vereditos_v403']:
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
        P.append('a v404 cria exatamente as chaves %s com veredito no core e o core traz %s' % (sorted(REG_FIXOS), sorted(novos)))
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
        e401_ = ESP.get('veredito_da_falsidade_v403') if k == 'falsidade_da_inercia_v401' else (ESP.get('registros_v401') or {}).get(k)
        if not e401_ or r.get('verdict') != e401_:
            P.append('%s: o veredito do rito difere do ensaio a seco' % k)
    V['reg402'] = list(REG_V402); V['reg402_estado'] = {}
    for k in REG_V402:    # os CINCO registros da v402 sao RECRIADOS pelo rito: tem de seguir no core, selados e (por veredito) iguais ao que a v403 selou (ESPERADOS[vereditos_v403])
        r = core.get(k)
        if not (isinstance(r, dict) and 'verdict' in r):
            P.append('registro obrigatorio ausente do core: %s' % k)
            continue
        V['reg402_estado'][k] = {'verdict': r.get('verdict'), 'ok': r.get('all_verified')}
        if r.get('all_verified') is not True:
            P.append('%s nao selou' % k)
        if GUARDA.search(str(r.get('verdict') or '')):
            P.append('%s com palavra proibida' % k)
        e402_ = (ESP.get('vereditos_v403') or {}).get(k)
        if not e402_ or r.get('verdict') != e402_:
            P.append('%s: o veredito do rito difere do ensaio a seco' % k)
    V['reg403'] = list(REG_V403); V['reg403_estado'] = {}
    for k in REG_V403:    # os SEIS registros da v403 sao RECRIADOS pelo rito: tem de seguir no core, selados e (por veredito) iguais ao que a v403 selou (ESPERADOS[vereditos_v403])
        r = core.get(k)
        if not (isinstance(r, dict) and 'verdict' in r):
            P.append('registro obrigatorio ausente do core: %s' % k)
            continue
        V['reg403_estado'][k] = {'verdict': r.get('verdict'), 'ok': r.get('all_verified')}
        if r.get('all_verified') is not True:
            P.append('%s nao selou' % k)
        if GUARDA.search(str(r.get('verdict') or '')):
            P.append('%s com palavra proibida' % k)
        e403_ = (ESP.get('vereditos_v403') or {}).get(k)
        if not e403_ or r.get('verdict') != e403_:
            P.append('%s: o veredito do rito difere do ensaio a seco' % k)
    for k in V['troca_dita']:
        r = core.get(k) or {}
        if r.get('all_verified') is False:
            P.append('%s (troca dita) nao selou' % k)
    # v404: o modulo novo de kernel vem de ESPERADOS[pedras_sha256] (o ensaio a seco do candidato) e e' conferido AQUI contra o arquivo do kernel do Nos (sha256); o numero tem de ser o de kernel_modulos_novos_v404.json
    if PK not in sys.path:
        sys.path.insert(0, PK)
    import delta_v404 as DL_   # STONES (key, rel), REGISTRO_DE_PEDRA, REGISTROS_FUNCAO, N_CHECKS, N_CHECKS_FALSIDADE, ERRATAS_V404, VERBATIM_CHAVE_PREFIXO_V404: lidos do delta, nunca digitados aqui
    REL_ = {s_['key']: s_['rel'] for s_ in DL_.STONES}; KEY_DE_REL_ = {v_: k_ for k_, v_ in REL_.items()}
    if list(REG_FUNCAO) != list(DL_.REGISTROS_FUNCAO) or dict(PEDRA_DE) != dict(DL_.REGISTRO_DE_PEDRA) or set(REL_) != set(PEDRA_DE):
        P.append('os nomes dos registros com funcao ou das pedras em leitura_v404.py != delta_v404.py (REGISTROS_FUNCAO, REGISTRO_DE_PEDRA, STONES)')
    V['pedras'] = []
    for rel_, h_ in list((ESP.get('pedras_sha256') or {}).items()):    # a ordem de ESPERADOS: projecao, jo8v32
        pth_ = os.path.join(NOS, 'tgl_kernel', *rel_.split('/'))
        shaf_ = sha(pth_) if os.path.isfile(pth_) else None
        V['pedras'].append({'key': KEY_DE_REL_.get(rel_), 'modulo': 'TGLExt.' + rel_[len('TGLExt/'):-len('.lean')].replace('/', '.'), 'rel': rel_, 'sha16': (shaf_ or '')[:16], 'sha256': shaf_, 'bytes': os.path.getsize(pth_) if os.path.isfile(pth_) else None,
                            'bandeiras': ((ESP.get('pedras') or {}).get(rel_) or {}).get('bandeiras'), 'decl': None, 'ok': bool(rel_.startswith('TGLExt/') and rel_.endswith('.lean') and shaf_ == h_)})
    V['n_pedras'] = len(V['pedras'])
    njp_ = os.path.join(PK, 'kernel_modulos_novos_v404.json'); nj_ = json.load(open(njp_, encoding='utf-8')) if os.path.exists(njp_) else {}
    n_esperado_ = nj_.get('novos') if isinstance(nj_.get('novos'), int) else len(nj_.get('novos') or [])
    if not V['n_pedras'] or V['n_pedras'] != n_esperado_ or any(p['ok'] is not True for p in V['pedras']):
        P.append('modulos novos do kernel: numero (%s) != kernel_modulos_novos_v404.json (%s) ou algum arquivo do Nos difere do sha256 de ESPERADOS[pedras_sha256]' % (V['n_pedras'], n_esperado_))
    vs = core.get('varredura_e_sorry_v392') or {}
    V['varr'] = vs.get('varredura') or {}; V['varr_verdict'] = vs.get('verdict')
    V['axiom_report_n'] = len((core.get('kernel_formalization') or {}).get('axiom_report') or {})
    ep = core.get('estatuto_da_prova_v391') or {}
    V['ep_verdict'] = ep.get('verdict')
    V['fd390'] = (core.get('fundacao_v390') or {}).get('verdict')
    V['verbatins'] = {k: {'sha16': str(v.get('sha256'))[:16], 'bytes': v.get('bytes')} for k, v in (ESP.get('cunhagens') or {}).items()}
    # --- v404: os CINCO registros novos (tres com FUNCAO, dois por spec) conferidos contra o ensaio a seco registrado em ESPERADOS; os da v398, da v397, da v396, da v395, da v394 e da v393 seguem no core e tem de seguir selados (os da v403, da v402, da v401 e da v399 sao recriados e conferidos acima); o sidecar; nenhum numero e' digitado
    V['reg_todos'] = list(REG_TODOS)
    for k_ in REG_V393 + REG_V394 + REG_V395 + REG_V396 + REG_V397 + REG_V398:
        if (core.get(k_) or {}).get('all_verified') is not True:
            P.append('%s (registro da v398, da v397, da v396, da v395, da v394 ou da v393) deixou de selar' % k_)
    RV_ = dict(ESP.get('vereditos_novos_v404') or {})   # registro -> veredito do ensaio a seco (projecao_transversal, jo8v32 e f2b_errata sao runtime; cunhagens_v404 e kh_n1_cobertura_v404 sao por spec)
    V['reg404'] = {}
    for k_ in REG_FIXOS:
        r_ = core.get(k_) or {}
        V['reg404'][k_] = {'verdict': r_.get('verdict'), 'ok': r_.get('all_verified')}
        esp_v_ = RV_.get(k_)
        if esp_v_ is None:
            P.append('ESPERADOS_v404 nao traz o veredito do ensaio a seco de %s (vereditos_novos_v404): nao ha com que conferir' % k_)
        elif r_.get('verdict') != esp_v_:
            P.append('%s: o veredito do rito difere do ensaio a seco' % k_)
    kf_ = (core.get('kernel_formalization') or {})
    rf_ = core.get('rede_fock_v394') or {}   # limite dito: o contrato conjunto da rede segue NAO habitado (a face de Fock do psion depende dele)
    if rf_.get('whole_certificate_inhabited') is not False:
        P.append('rede_fock_v394: whole_certificate_inhabited deve seguir False (o contrato conjunto da rede segue aberto) e o core traz %r' % (rf_.get('whole_certificate_inhabited'),))
    if kf_.get('ext_bin394_0001') is not True:
        P.append('a bandeira da pedra da v394 (ext_bin394_0001) nao segue True no kernel do rito')
    # a face de Fock do psion segue como a v395 a selou: CONDICIONAL, sem habitante exibido, com a bandeira True e declarada em Psibit.lean (nem a v396, nem a v397, nem a v403, nem a v404 a habitam)
    pb_ = core.get('psibit_v395') or {}; pbc_ = pb_.get('conditional_psion_face') or {}
    if not (pbc_.get('status') == 'CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE' and pbc_.get('inhabitant_exhibited') is False and pbc_.get('flag_true') is True and kf_.get(pbc_.get('flag')) is True and pbc_.get('declared_in') == 'TGLExt/Psibit.lean'):
        P.append('psibit_v395: a face do psion deixou de estar como CONDICIONAL sem habitante exibido (bandeira True, declarada em TGLExt/Psibit.lean)')
    fkb_ = ((_base_core(PK).get('testemunha_estatica_v396') or {}).get('fock_face') or {})   # o que a v403 SELADA diz (copia de bytes): o teorema e o modulo da face de Fock, lidos, nao digitados
    te_ = core.get('testemunha_estatica_v396') or {}; fk_ = te_.get('fock_face') or {}
    if not (fk_.get('status') == 'CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE' and fk_.get('inhabitant_exhibited') is False and fk_.get('declared_outside_the_stone') is True and fk_.get('linked_to_the_corner_by_a_lemma') is False
            and fkb_.get('theorem') and fk_.get('theorem') == fkb_.get('theorem') and fkb_.get('declared_in') and fk_.get('declared_in') == fkb_.get('declared_in')):
        P.append('testemunha_estatica_v396: a face de Fock do psion deixou de estar como CONDICIONAL, declarada em Psibit.lean fora da pedra e sem habitante exibido')
    # o registro teste_de_veracidade_fase9_v397 (o QUADRO do topo le os numeros dele): segue selado e igual, conferido por inteiro (os textos leem os numeros dele; NENHUM sigma e' calculado aqui)
    tv_ = core.get('teste_de_veracidade_fase9_v397') or {}; EV_ = ESP.get('veracidade') or {}
    ck_ = tv_.get('checks') or []; fo_ = {f_.get('chave'): f_ for f_ in (tv_.get('fontes') or []) if isinstance(f_, dict)}
    num_ = EV_.get('numeros_do_resultado') or {}; lido_ = tv_.get('lido') or {}
    nums_ok_ = bool(num_) and all(lido_.get(k_) == v_ for k_, v_ in num_.items())
    fontes_ok_ = bool(EV_.get('fontes')) and all((fo_.get(c_) or {}).get('sha256') == h_ and (fo_.get(c_) or {}).get('ok') is True for c_, h_ in EV_['fontes'].items())
    V['veracidade'] = {'verdict': tv_.get('verdict'), 'ok': tv_.get('all_verified'), 'n_checks': len(ck_), 'checks_ok': bool(ck_) and all(c_.get('ok') is True for c_ in ck_), 'lido': lido_, 'numeros_ok': nums_ok_,
                       'fontes': {c_: str(f_.get('sha256') or '') for c_, f_ in fo_.items()}, 'fontes_ok': fontes_ok_, 'does_not_gate_core': tv_.get('does_not_gate_core')}
    if not (tv_.get('all_verified') is True and tv_.get('does_not_gate_core') is True and len(ck_) == EV_.get('n_checks') and V['veracidade']['checks_ok'] and nums_ok_ and fontes_ok_ and tv_.get('verdict') == (ESP.get('vereditos_v403') or {}).get('teste_de_veracidade_fase9_v397')):
        P.append('teste_de_veracidade_fase9_v397 nao selou inteiro (selo, checagens, numeros lidos == ESPERADOS[veracidade], fontes por sha256): ver o registro no core')
    zd_, pw_ = lido_.get('z_disc_calibrado'), lido_.get('poder_previo')
    if not (isinstance(zd_, float) and zd_ < 5.0 and isinstance(pw_, float) and pw_ >= 5.0):
        P.append('o z_disc calibrado nao esta abaixo de 5 ou o poder previo nao e de 5 sigma ou mais (%r, %r): os textos e o quadro dizem que o degrau de 5 sigma da creditacao nao foi alcancado e que a TGL nao foi falsificada com poder' % (zd_, pw_))
    if PK not in sys.path:
        sys.path.insert(0, PK)
    try:
        import quadro_v397 as QV_
        rp_ = _res_path(EV_)
        rb_ = open(rp_, 'rb').read()
        if hashlib.sha256(rb_).hexdigest() != (EV_.get('fontes') or {}).get('f9v2_resultado'):
            P.append('o resultado pinado do Teste da Unica Palavra != o sha256 de ESPERADOS[veracidade][fontes][f9v2_resultado]')
        else:
            lr_ = QV_.lido_do_resultado(json.loads(rb_.decode('utf-8')))
            if not lr_ or any(lr_.get(k_) != lido_.get(k_) for k_ in lr_):
                P.append('os numeros que o registro leu != os do resultado pinado (lidos pelos mesmos caminhos de delta_v404.F9_CAMINHOS)')
        if QV_.Q._v397_atomos(tv_, 'pt').get('sealed') is not True or QV_.Q._v397_atomos(tv_, 'en').get('sealed') is not True:
            P.append('o quadro do Teste da Unica Palavra nao sela (algum numero ausente ou o registro nao selou): o artigo diria que o registro nao selou')
    except Exception as e_:   # noqa: BLE001
        P.append('nao consegui conferir o registro do Teste da Unica Palavra contra o resultado pinado: %r' % (e_,))
    # as DUAS pedras (ProjecaoTransversalDaMeiaNat, Jo8v32) no kernel do rito: bandeira True, composicao incondicional e estrela no trio, proveniencia no modulo da pedra, contrato e suporte no trio e no modulo certo, sha256 da fonte no hash formal; tudo contra ESPERADOS; nenhum numero e' digitado
    TRIO_ = {'propext', 'Classical.choice', 'Quot.sound'}
    axr_ = kf_.get('axiom_report') or {}; src_ = kf_.get('declaration_sources_v394') or {}
    em_trio_ = lambda n_: bool(isinstance(axr_.get(n_), list) and set(axr_.get(n_)) <= TRIO_)
    V['h8'] = len(kf_.get('formal_files_sha256') or {})
    if V['h8'] != ESP.get('h8_entradas') or not all(r_ in (kf_.get('formal_files_sha256') or {}) for r_ in (ESP.get('h8_residuais_do_nos') or [])):
        P.append('o hash formal do rito tem %s entradas (ESPERADOS[h8_entradas] = %s) ou lhe falta um residual do Nos' % (V['h8'], ESP.get('h8_entradas')))
    V['pedras_kernel'] = {}; kernel_ok_ = {}; estrela_ok_ = {}; est_ = {}; flag_true_ = {}
    for k_ in PEDRA_DE:
        rel_k_ = REL_.get(k_)
        th_ = (ESP.get('teoremas_das_pedras') or {}).get(k_); fl_ = (ESP.get('bandeiras_das_pedras') or {}).get(k_)
        est_[k_] = (ESP.get('estrelas_v404') or {}).get(k_) or {}
        contrato_ = (ESP.get('contrato_das_pedras') or {}).get(k_) or []; suporte_ = (ESP.get('suporte_das_pedras') or {}).get(k_) or {}
        contrato_ok_ = bool(contrato_) and all(em_trio_(t_) and src_.get(t_) == rel_k_ for t_ in contrato_)
        suporte_ok_ = bool(suporte_) and all(em_trio_(t_) and src_.get(t_) == p_ for t_, p_ in suporte_.items())
        flag_true_[k_] = bool(fl_) and kf_.get(fl_) is True
        estrela_ok_[k_] = bool(est_[k_].get('teorema') and est_[k_].get('bandeira') and kf_.get(est_[k_].get('bandeira')) is True and em_trio_(est_[k_].get('teorema')) and src_.get(est_[k_].get('teorema')) == rel_k_)
        kernel_ok_[k_] = bool(th_ and fl_ and rel_k_ and flag_true_[k_] and em_trio_(th_) and src_.get(th_) == rel_k_ and contrato_ok_ and suporte_ok_ and estrela_ok_[k_]
                              and (kf_.get('formal_files_sha256') or {}).get(rel_k_) == (ESP.get('pedras_sha256') or {}).get(rel_k_))
        V['pedras_kernel'][k_] = {'rel': rel_k_, 'flag': fl_, 'flag_true': flag_true_[k_], 'theorem': th_, 'axioms': axr_.get(th_), 'source': src_.get(th_), 'contrato_ok': contrato_ok_, 'suporte_ok': suporte_ok_, 'estrela_ok': estrela_ok_[k_], 'kernel_ok': kernel_ok_[k_],
                                  'n_contrato': len(contrato_), 'n_suporte': len(suporte_), 'estrela': (est_[k_].get('teorema'), est_[k_].get('bandeira'))}
        if not kernel_ok_[k_]:
            P.append('a pedra %s nao esta no kernel do rito como o ensaio a seco a pinou (bandeira True, composicao incondicional e estrela no trio, proveniencia no modulo da pedra, contrato e suporte no trio e no modulo certo, sha256 da fonte no hash formal)' % os.path.basename(rel_k_ or 'x.lean')[:-len('.lean')])
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
    # os DOIS registros com FUNCAO das pedras da v404 (projecao, jo8v32): conferidos por inteiro contra ESPERADOS[registros_funcao_v404] e contra as pedras no kernel do rito (a mesma conferencia de conferir_rito_v404, mais a ligacao com a composicao e a estrela de ESPERADOS)
    for k_, nome_ in PEDRA_DE.items():
        R_ = core.get(nome_) or {}; E_ = (ESP.get('registros_funcao_v404') or {}).get(k_) or {}
        mech_ = R_.get('mechanics') or {}; vv_ = R_.get('values') or {}; n_ck_ = DL_.N_CHECKS.get(k_)
        mech_ok_k_ = bool(mech_.get('passed') is True and mech_.get('n_checks') == n_ck_ == E_.get('n_checks') and len(mech_.get('checks') or []) == n_ck_ and all(c_.get('ok') is True for c_ in (mech_.get('checks') or [])))
        values_ok_k_ = bool(vv_ and E_.get('values') and set(E_['values']) <= set(vv_) and _feq({kk_: vv_.get(kk_) for kk_ in E_['values']}, E_['values']))
        beta_ok_k_ = bool(R_.get('beta_ok') is True and isinstance(vv_.get('beta'), float) and isinstance(b0_, float) and abs(vv_['beta'] - b0_) <= 1e-9 * abs(b0_))
        ctx_ok_k_ = bool((R_.get('context') or {}).get('ok') is True and (R_.get('context') or {}).get('text_in_embedded_kernel') is True)
        un_ = R_.get('unconditional') or {}; kt_ = R_.get('key_theorem') or {}
        unc_ok_k_ = bool(un_.get('in_kernel') is True and un_.get('flag_true') is True and un_.get('theorem') == (ESP.get('teoremas_das_pedras') or {}).get(k_) and un_.get('flag') == (ESP.get('bandeiras_das_pedras') or {}).get(k_) and un_.get('axioms') is not None and set(un_.get('axioms') or []) <= TRIO_)
        key_ok_k_ = bool(kt_.get('in_kernel') is True and kt_.get('flag_true') is True and kt_.get('theorem') == est_[k_].get('teorema') and kt_.get('flag') == est_[k_].get('bandeira'))
        sealed_k_ = bool(R_.get('all_verified') is True and R_.get('does_not_gate_core') is True and R_.get('runtime_executed') is True and bool(E_.get('verdict')) and R_.get('verdict') == E_.get('verdict') and mech_ok_k_ and values_ok_k_ and beta_ok_k_ and ctx_ok_k_ and unc_ok_k_ and key_ok_k_
                         and kernel_ok_[k_] and not GUARDA.search(str(R_.get('verdict') or '')))
        V[k_] = {'registro': nome_, 'verdict': R_.get('verdict'), 'ok': R_.get('all_verified'), 'sealed': sealed_k_, 'n_checks': mech_.get('n_checks'), 'mech_ok': mech_ok_k_, 'values': vv_, 'values_ok': values_ok_k_, 'beta_ok': beta_ok_k_, 'kernel_ok': kernel_ok_[k_], 'estrela_ok': estrela_ok_[k_],
                 'contexto_ok': ctx_ok_k_, 'unconditional_ok': unc_ok_k_, 'key_ok': key_ok_k_, 'flag': (ESP.get('bandeiras_das_pedras') or {}).get(k_), 'flag_true': flag_true_[k_], 'theorem': (ESP.get('teoremas_das_pedras') or {}).get(k_), 'estrela': (est_[k_].get('teorema'), est_[k_].get('bandeira')),
                 'runtime_executed': R_.get('runtime_executed'), 'does_not_gate_core': R_.get('does_not_gate_core')}
        if not sealed_k_:
            P.append('%s nao selou inteiro (selo, as %s checagens do calculo, valores == ESPERADOS[registros_funcao_v404], beta == alfa x raiz de e do core, o texto-contexto no kernel embutido, a composicao (bandeira True) e a estrela no kernel do rito e no trio, contrato e suporte da pedra, nao move o gate): ver o registro no core' % (nome_, n_ck_))
    # a errata de F2b (registro com FUNCAO, SEM pedra): o V1 do ramo B lido por hash e como antes, o livro v383 intacto, a calibracao A e a previsao do par LIDAS do V1, a previsao fora do intervalo de A e de sinal oposto, nenhum desfecho; o canal passa de AWAITING a retirado antes do dado AO LADO
    fb_ = core.get('f2b_errata_v404') or {}; EFB_ = RF_.get('f2b') or {}; fbm_ = fb_.get('mechanics') or {}; fbv_ = fb_.get('values') or {}
    rbc_ = core.get('ramo_b_preregistration_v386') or {}; ldc_ = (core.get('ledger_errata_v386') or {}).get('charge_F2b') or {}; rbb_ = _base_core(PK).get('ramo_b_preregistration_v386') or {}; ldb_ = (_base_core(PK).get('ledger_errata_v386') or {}).get('charge_F2b') or {}
    f2b_mech_ok_ = bool(fbm_.get('passed') is True and fbm_.get('n_checks') == DL_.N_CHECKS['f2b'] == EFB_.get('n_checks') and len(fbm_.get('checks') or []) == DL_.N_CHECKS['f2b'] and all(c_.get('ok') is True for c_ in (fbm_.get('checks') or [])))
    f2b_values_ok_ = bool(fbv_ and EFB_.get('values') and set(EFB_['values']) <= set(fbv_) and _feq({kk_: fbv_.get(kk_) for kk_ in EFB_['values']}, EFB_['values']))
    f2b_beta_ok_ = bool(fb_.get('beta_ok') is True and isinstance(fbv_.get('beta'), float) and isinstance(b0_, float) and abs(fbv_['beta'] - b0_) <= 1e-9 * abs(b0_))
    f2b_ao_lado_ok_ = bool(fb_.get('F2b_status_before') == 'AWAITING' and fb_.get('F2b_status_now') == DL_.F2B_FUTURO_TOKEN == (ESP.get('f2b_depois') or {}).get('F2b_status_now') and fb_.get('channel_token_now') == DL_.F2B_FUTURO_TOKEN and fb_.get('v1_token_kept') == DL_.F2B_V1_TOKEN_ANTIGO
                           and rbc_.get('F2b_status') == (ESP.get('f2b_antes') or {}).get('F2b_status') and rbc_.get('veredito_do_V1') == (ESP.get('f2b_antes') or {}).get('veredito_do_V1') and bool(rbb_) and _feq(rbc_, rbb_) and bool(ldb_) and _feq(ldc_, ldb_) and ldc_.get('token') == (ESP.get('f2b_antes') or {}).get('charge_F2b_token'))
    nmc_ = core.get('neutrino_mass') or {}
    neutrino_intacto_ = bool(hashlib.sha256(str(nmc_.get('angle_status') or '').encode('utf-8')).hexdigest() == ESP.get('neutrino_angle_status_antigo_sha256') and nmc_.get('frozen_hash') == ESP.get('neutrino_frozen_hash_v403') and nmc_.get('verdict') == (ESP.get('vereditos_v403') or {}).get('neutrino_mass'))
    f2b_ok_ = bool(fb_.get('all_verified') is True and fb_.get('does_not_gate_core') is True and fb_.get('runtime_executed') is True and bool(EFB_.get('verdict')) and fb_.get('verdict') == EFB_.get('verdict') and f2b_mech_ok_ and f2b_values_ok_ and f2b_beta_ok_ and f2b_ao_lado_ok_ and neutrino_intacto_
                   and not fb_.get('guarda_p18_violacoes') and not GUARDA.search(str(fb_.get('verdict') or '')))
    V['f2b'] = {'registro': 'f2b_errata_v404', 'verdict': fb_.get('verdict'), 'ok': fb_.get('all_verified'), 'sealed': f2b_ok_, 'n_checks': fbm_.get('n_checks'), 'mech_ok': f2b_mech_ok_, 'values': fbv_, 'values_ok': f2b_values_ok_, 'beta_ok': f2b_beta_ok_, 'ao_lado_ok': f2b_ao_lado_ok_,
                'neutrino_intacto': neutrino_intacto_, 'status_antes': fb_.get('F2b_status_before'), 'status_agora': fb_.get('F2b_status_now'), 'token_v1': fb_.get('v1_token_kept'), 'runtime_executed': fb_.get('runtime_executed'), 'does_not_gate_core': fb_.get('does_not_gate_core')}
    if not f2b_ok_:
        P.append('f2b_errata_v404 nao selou inteiro (selo, as %s checagens do registro, valores == ESPERADOS[registros_funcao_v404][f2b], beta == alfa x raiz de e do core, o V1 do ramo B, o registro da v386 e a cobranca F2b da v386 IGUAIS aos da v403 selada [a errata e\' AO LADO], o canal agora retirado antes do dado, '
                 'a funcao do neutrino intacta [angle_status antigo, frozen_hash e veredito], nenhum desfecho, nao move o gate): ver o registro no core' % DL_.N_CHECKS['f2b'])
    # as BANDEIRAS DO GATE (F8.1 da v403; registro com FUNCAO bandeiras_do_gate_v403, RECRIADO pelo rito da v404): conferido por inteiro contra ESPERADOS[registros_funcao_v403][gate] (as checagens e os valores == os do core da v403 selada) e RELIDO aqui no core do rito, independente do registro (as tres fontes das bandeiras antes literais, os seis checks do gate da v403 mais a sonda, a letra do veredito)
    gk_ = core.get('bandeiras_do_gate_v403') or {}; EG_ = RF3_.get('gate') or {}; gm_ = gk_.get('mechanics') or {}; gv_ = gk_.get('values') or {}
    gmech_ok_ = bool(gm_.get('passed') is True and gm_.get('n_checks') == DL_.D3.N_CHECKS['gate'] == EG_.get('n_checks') and len(gm_.get('checks') or []) == DL_.D3.N_CHECKS['gate'] and all(c_.get('ok') is True for c_ in (gm_.get('checks') or [])))
    gvalues_ok_ = bool(gv_ and EG_.get('values') and set(EG_['values']) <= set(gv_) and _feq({kk_: gv_.get(kk_) for kk_ in EG_['values']}, EG_['values']))
    qgx_ = core.get('qg_closure') or {}
    n18x_ = sum(1 for fam_ in ('formal_flags', 'physics_flags', 'experiment_flags') for v_ in (qgx_.get(fam_) or {}).values() if v_ is True)
    ls2x_ = sorted(k_ for k_ in kf_ if k_.startswith(DL_.F81_PREFIXO_LS2))
    prex_ = [c_[1] for c_ in ((core.get('void_floor_v11') or {}).get('checks') or []) if isinstance(c_, (list, tuple)) and len(c_) == 2 and c_[0] == DL_.F81_ROTULO_PREREG]
    ck_old_ = [list(c_) for c_ in (ESP.get('qg_closure_v403_checks') or [])]; ck_new_ = [list(c_) for c_ in (qgx_.get('checks') or [])]
    sonda_ = [c_ for c_ in ck_new_ if str(c_[0]).startswith('ProbeBlindNullAbsent')]
    f81x_ok_ = bool(len(ls2x_) == 6 and all(kf_.get(k_) is True for k_ in ls2x_) and (qgx_.get('physics_flags') or {}).get('linearized_spin2_finite_face') is True and len(prex_) == 1 and prex_[0] is True and (qgx_.get('experiment_flags') or {}).get('protocol_pre_registered') is True
                    and (core.get('void_stacking_blind') or {}).get('all_verified') is True and (qgx_.get('experiment_flags') or {}).get('null_tests_passed_blind') is True and n18x_ == 18
                    and len(ck_old_) == 7 and ck_new_ == ck_old_ and len(sonda_) == 1 and all(c_[1] is True for c_ in ck_new_)
                    and (qgx_.get('gate') or {}).get('verdict') == ESP.get('qg_closure_gate_verdict_v403') == selo.get('qg_closure_verdict'))
    gate_ok_ = bool(gk_.get('all_verified') is True and gk_.get('does_not_gate_core') is True and gk_.get('runtime_executed') is True and bool(EG_.get('verdict')) and gk_.get('verdict') == EG_.get('verdict') and gmech_ok_ and gvalues_ok_ and f81x_ok_
                    and gv_.get('n_flags') == 18 == gv_.get('n_true') == gv_.get('n_calculated') and gv_.get('n_literal') == 0 and gv_.get('n_read_by_the_verdict') == 15 and gv_.get('read_by_the_verdict') == [6, 5, 4] and gv_.get('gate_verdict_equals_v402') is True
                    and not GUARDA.search(str(gk_.get('verdict') or '')))
    V['gate'] = {'registro': 'bandeiras_do_gate_v403', 'verdict': gk_.get('verdict'), 'ok': gk_.get('all_verified'), 'sealed': gate_ok_, 'n_checks': gm_.get('n_checks'), 'mech_ok': gmech_ok_, 'values': gv_, 'values_ok': gvalues_ok_, 'f81_ok': f81x_ok_, 'n18': n18x_, 'n_ls2': len(ls2x_),
                 'n_checks_do_gate': len(ck_new_), 'sonda': len(sonda_), 'runtime_executed': gk_.get('runtime_executed'), 'does_not_gate_core': gk_.get('does_not_gate_core')}
    if not gate_ok_:
        P.append('bandeiras_do_gate_v403 nao selou inteiro (selo, as %s checagens do registro, valores == ESPERADOS[registros_funcao_v403][gate], 18 bandeiras True e TODAS calculadas, 15 no veredito (6+5+4), a releitura aqui das tres fontes da F8.1 [a familia ext_ls2_* do kernel, a checagem «pre-registro v67 INTACTO (hash)» do rito V11, o teste nulo cego], '
                 'os sete checks do gate (os seis da v403 mais a sonda ProbeBlindNullAbsent) IGUAIS aos da v403 selada, a letra do veredito do gate == a da v403 e a do selo, nao move o gate): ver o registro no core' % DL_.D3.N_CHECKS['gate'])
    # os registros com FUNCAO da v402 (ponte, queda, esperanca) e da v403 (caminho, vida, verdade_adendo) RECRIADOS pelo rito: iguais ao que a v403 SELOU (veredito == ESPERADOS[vereditos_v403]; as checagens e os valores do calculo == os do core selado em base_v403), selados, com a composicao e a estrela no kernel do rito e no trio
    for fkey_, FUN_ in (('fun402', FUN_V402), ('fun403', FUN_V403)):
        V[fkey_] = {}
        for k_, nome_ in FUN_.items():
            R_ = core.get(nome_) or {}; B_ = _base_core(PK).get(nome_) or {}; mech_ = R_.get('mechanics') or {}; vv_ = R_.get('values') or {}
            mech_ok_k_ = bool(mech_.get('passed') is True and bool(B_) and _feq(mech_, B_.get('mechanics')))
            values_ok_k_ = bool(vv_ and (B_.get('values') or {}) and _feq(vv_, B_['values']))
            beta_ok_k_ = bool(R_.get('beta_ok') is True and isinstance(vv_.get('beta'), float) and isinstance(b0_, float) and abs(vv_['beta'] - b0_) <= 1e-9 * abs(b0_))
            un_ = R_.get('unconditional') or {}; kt_ = R_.get('key_theorem') or {}
            kern_ok_k_ = bool(un_.get('in_kernel') is True and kt_.get('in_kernel') is True and kf_.get(un_.get('flag')) is True and kf_.get(kt_.get('flag')) is True and em_trio_(un_.get('theorem')) and em_trio_(kt_.get('theorem')) and (R_.get('context') or {}).get('ok') is True)
            sealed_k_ = bool(R_.get('all_verified') is True and R_.get('does_not_gate_core') is True and R_.get('runtime_executed') is True and bool(EV2_.get(nome_)) and R_.get('verdict') == EV2_.get(nome_) and mech_ok_k_ and values_ok_k_ and beta_ok_k_ and kern_ok_k_ and not GUARDA.search(str(R_.get('verdict') or '')))
            V[fkey_][k_] = {'registro': nome_, 'verdict': R_.get('verdict'), 'ok': R_.get('all_verified'), 'sealed': sealed_k_, 'n_checks': mech_.get('n_checks'), 'mech_ok': mech_ok_k_, 'values_ok': values_ok_k_, 'beta_ok': beta_ok_k_, 'kernel_ok': kern_ok_k_}
            if not sealed_k_:
                P.append('%s nao selou inteiro (recriado pelo rito: selo, veredito == o da v403 selada, as checagens e os valores do calculo == os da v403 selada [base_v403], beta == alfa x raiz de e do core, a composicao e a estrela no kernel do rito e no trio, nao move o gate): ver o registro no core' % nome_)
    # as TRES pedras SELADAS da v403 seguem no kernel do Nos com o sha256 da v403 (registro: pedra selada nao se renomeia por cima)
    V['pedras_v403'] = {}
    for rel_, h_ in (ESP.get('pedras_v403_sha256') or {}).items():
        pth_ = os.path.join(NOS, 'tgl_kernel', *rel_.split('/')); shaf_ = sha(pth_) if os.path.isfile(pth_) else None
        V['pedras_v403'][rel_] = {'sha16': (shaf_ or '')[:16], 'ok': bool(shaf_ == h_ and (kf_.get('formal_files_sha256') or {}).get(rel_) == h_)}
    if len(V['pedras_v403']) != 3 or any(p_['ok'] is not True for p_ in V['pedras_v403'].values()):
        P.append('as pedras seladas da v403 (Caminho, Vida, VerdadeAdendo) deixaram de estar no kernel do Nos com o sha256 da v403 (registro: pedra selada nao se renomeia por cima)')
    # a falsidade da inercia (v401, registro com FUNCAO) RECRIADA pelo rito: igual ao ensaio a seco (veredito) e a v403 SELADA (valores e checagens do calculo), com a composicao e a estrela no kernel do rito
    fa_ = core.get('falsidade_da_inercia_v401') or {}; fm_ = fa_.get('mechanics') or {}; fvv_ = fa_.get('values') or {}
    fab_ = _base_core(PK).get('falsidade_da_inercia_v401') or {}   # a falsidade da v403 SELADA (copia de bytes em base_v403): a recriada tem de dar os mesmos valores
    values_f_ok_ = bool(fvv_ and (fab_.get('values') or {}) and _feq(fvv_, fab_['values']) and _feq(fm_, fab_.get('mechanics')))
    mech_ok_ = bool(fm_.get('passed') is True and fm_.get('n_checks') == DL_.N_CHECKS_FALSIDADE and len(fm_.get('checks') or []) == DL_.N_CHECKS_FALSIDADE and all(c_.get('ok') is True for c_ in (fm_.get('checks') or [])))
    beta_f_ok_ = bool(fa_.get('beta_ok') is True and isinstance(fvv_.get('beta'), float) and isinstance(b0_, float) and abs(fvv_['beta'] - b0_) <= 1e-9 * abs(b0_))
    hy_ = fa_.get('named_hypothesis') or {}
    chain_ok_ = bool('DERIVED' in str(fa_.get('chain_status')) and hy_.get('name') == 'H_tau' and hy_.get('status') == 'OPEN' and hy_.get('used_by_a_theorem') is False and isinstance(fvv_.get('min_weight_on_the_grid_positive'), float) and fvv_['min_weight_on_the_grid_positive'] > 0.0
                     and fvv_.get('diag_flow_gap_zero_is_fixed') is True and bool(fvv_.get('abyss_witnesses')) and bool(fvv_.get('leak_witnesses_g_half')))
    fu_ = fa_.get('unconditional') or {}; fkt_ = fa_.get('key_theorem') or {}
    kernel_f_ok_ = bool(fu_.get('in_kernel') is True and fkt_.get('in_kernel') is True and fu_.get('theorem') and fkt_.get('theorem') and kf_.get(fu_.get('flag')) is True and kf_.get(fkt_.get('flag')) is True and em_trio_(fu_.get('theorem')) and em_trio_(fkt_.get('theorem')))
    fal_ok_ = bool(chain_ok_ and fa_.get('all_verified') is True and fa_.get('does_not_gate_core') is True and fa_.get('runtime_executed') is True and bool(ESP.get('veredito_da_falsidade_v403')) and fa_.get('verdict') == ESP.get('veredito_da_falsidade_v403') and mech_ok_ and values_f_ok_ and beta_f_ok_
                   and (fa_.get('costless') or {}).get('ok') is True and kernel_f_ok_ and not GUARDA.search(str(fa_.get('verdict') or '')))
    V['fal401'] = {'verdict': fa_.get('verdict'), 'ok': fa_.get('all_verified'), 'sealed': fal_ok_, 'n_checks': fm_.get('n_checks'), 'mech_ok': mech_ok_, 'values_ok': values_f_ok_, 'beta_ok': beta_f_ok_, 'chain_ok': chain_ok_, 'kernel_ok': kernel_f_ok_,
                   'costless_ok': (fa_.get('costless') or {}).get('ok'), 'runtime_executed': fa_.get('runtime_executed'), 'does_not_gate_core': fa_.get('does_not_gate_core')}
    if not fal_ok_:
        P.append('falsidade_da_inercia_v401 nao selou inteiro (recriada pelo rito: selo, as checagens do calculo no modelo oneScaling (DL.N_CHECKS_FALSIDADE), a cadeia derivada [DERIVED], a hipotese H_tau [OPEN] nao usada por teorema, valores e checagens == os da v403 selada, beta == alfa x raiz de e do core, 0_abs de costless no kernel embutido, a composicao e a estrela no kernel do rito, nao move o gate): ver o registro no core')
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
    sr_ = selo.get('selo_pela_propria_tecnologia_v399') or {}; sdr_ = selo.get('declaracao_do_operador_v399') or {}; sreg_ = selo.get('registros_v399') or {}; sfr_ = selo.get('falsidade_da_inercia_v401') or {}; sreg1_ = selo.get('registros_v401') or {}; sreg2_ = selo.get('registros_v402') or {}; sreg3_ = selo.get('registros_v403') or {}; sreg4_ = selo.get('registros_v404') or {}
    resumos_ok_ = bool(sr_.get('verdict') == sa_.get('verdict') and sr_.get('all_verified') is True and sr_.get('sha256_do_um_py') == V['s64'] and sr_.get('does_not_gate_core') is True and sdr_.get('verdict') == dc_.get('verdict') and sdr_.get('all_verified') is True
                       and sdr_.get('verbatim_sha256') == EDC_.get('verbatim_sha256') and sdr_.get('does_not_gate_core') is True and bool(ESP.get('registros_v399')) and all((sreg_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') for k_ in ESP['registros_v399'])
                       and sfr_.get('verdict') == fa_.get('verdict') and bool(sfr_.get('verdict')) and sfr_.get('all_verified') is True and bool(ESP.get('registros_v401')) and all((sreg1_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and (sreg1_.get(k_) or {}).get('all_verified') is True for k_ in ESP['registros_v401'])
                       and all(((selo.get(n_) or {}).get('verdict') == (core.get(n_) or {}).get('verdict') and bool((selo.get(n_) or {}).get('verdict')) and (selo.get(n_) or {}).get('all_verified') is True and (selo.get(n_) or {}).get('does_not_gate_core') is True) for n_ in tuple(REG_FUNCAO) + tuple(FUN_V403.values()) + tuple(FUN_V402.values()) + ('bandeiras_do_gate_v403',))
                       and bool(ESP.get('registros_v402')) and all((sreg2_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg2_.get(k_) or {}).get('verdict')) and (sreg2_.get(k_) or {}).get('all_verified') is True for k_ in ESP['registros_v402'])
                       and bool(ESP.get('registros_v403')) and all((sreg3_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg3_.get(k_) or {}).get('verdict')) and (sreg3_.get(k_) or {}).get('all_verified') is True for k_ in ESP['registros_v403'])
                       and bool(ESP.get('registros_v404')) and all((sreg4_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') and bool((sreg4_.get(k_) or {}).get('verdict')) and (sreg4_.get(k_) or {}).get('all_verified') is True for k_ in ESP['registros_v404']))
    V['resumos_do_selo_ok'] = resumos_ok_
    if not resumos_ok_:
        P.append('o selo primario (um_absoluto_selo.json) nao traz os resumos do selo ACOM, da declaracao e dos registros por spec iguais aos do core')
    V['formais_nao_selados'] = sorted((selo.get('not_sealed_this_run') or {}).get('formais') or [])
    if V['formais_nao_selados'] != sorted(ESP.get('not_sealed_formais') or []):
        P.append('o selo traz modulo formal nao selado em not_sealed_this_run.formais (a recusa do selo ACOM so registra, mas o rito real tem de selar): %s' % V['formais_nao_selados'][:3])
    # cunhagens_v404: as NOVE falas do operador de 28/10 por sha256 (embedded_ok), todas do operador (nenhuma e' da gerencia), as erratas E7 a E9 (gerencia c1, em nome proprio), as decisoes D23 a D26, os nomes das duas pedras, a leitura da massa e o contrato das pedras
    cu = core.get('cunhagens_v404') or {}; kh = core.get('kh_n1_cobertura_v404') or {}
    cx_ = cu.get('extras') or {}; vb_ = cu.get('verbatim') or {}; ec_ = ESP.get('cunhagens') or {}
    aut_ = cx_.get('autor_de_cada_inscricao') or {}; pref_ = DL_.VERBATIM_CHAVE_PREFIXO_V404
    todas_op_ = bool(ec_ and len(aut_) == len(ec_) and set(aut_) == {k_[len(pref_):] for k_ in ec_} and all(a_ == 'operador' for a_ in aut_.values()) and 'leitura_da_gerencia' not in cx_ and not any(str(v_.get('papel', '')).startswith('leitura da gerencia') for v_ in ec_.values()))
    verb_ok_ = bool(ec_) and set(vb_) == set(ec_) and all((vb_[k_] or {}).get('sha256') == ec_[k_]['sha256'] and (vb_[k_] or {}).get('embedded_ok') is True for k_ in ec_)
    pares_ok_ = all(isinstance(x_, list) and len(x_) == 2 and x_[0] == x_[1] for x_ in (cu.get('kernel') or {}).values()) and bool(cu.get('kernel'))
    err_ = cu.get('erratas') or []; esp_err_ = list(ESP.get('erratas_E7_a_E9') or [])
    erratas_ok_ = bool(len(err_) == len(esp_err_) == len(DL_.ERRATAS_V404) == 3 and all(str(e_.get('assinatura', '')).startswith('gerencia c1, em nome proprio') for e_ in err_) and [e_.get('agora') for e_ in err_] == esp_err_
                       and cx_.get('erratas_E7_a_E9') == esp_err_ and str(cx_.get('assinatura', '')).startswith('gerencia c1, em nome proprio'))
    dec_ = cx_.get('decisoes_da_gerencia') or {}; exig_ = {'D%d' % i_ for i_ in range(23, 27)}
    decisoes_ok_ = bool(set(dec_) >= exig_ and dec_ == (ESP.get('decisoes_da_gerencia') or {None: None}) and all(str(dec_.get(d_) or '').strip() for d_ in exig_))
    nm_ = cx_.get('nomes') or {}
    nomes_ok_ = bool(all(str(nm_.get(k_) or '').strip() for k_ in ('projecao', 'jo8v32')))
    ms_ = cx_.get('leitura_massa_28out') or {}; ems_ = ESP.get('leitura_massa_28out') or {}
    massa_ok_ = bool(ems_ and ms_ == ems_)
    pv404_ = cx_.get('pedras_da_v403_como_registro') or {}; rels404_ = ('TGLExt/Caminho.lean', 'TGLExt/Vida.lean', 'TGLExt/VerdadeAdendo.lean')
    reg403_ok_ = bool(set(pv404_) == {'caminho', 'vida', 'verdade_adendo'} and all(r_ in (ESP.get('pedras_v403_sha256') or {}) for r_ in rels404_) and [pv404_.get(k_) for k_ in ('caminho', 'vida', 'verdade_adendo')] == [(ESP['pedras_v403_sha256'][r_])[:16] for r_ in rels404_])
    teor_ok_ = bool(cx_.get('teoremas') == ESP.get('teoremas_das_pedras') and cx_.get('bandeiras') == ESP.get('bandeiras_das_pedras') and cx_.get('n_bandeiras_por_pedra') == ESP.get('n_bandeiras_por_grupo') and cx_.get('n_bandeiras') == ESP.get('n_bandeiras_novas')
                    and cx_.get('cunhagens_embutidas') == len(ec_) and {k_: (v_ or {}).get('teorema') for k_, v_ in (ESP.get('estrelas_v404') or {}).items()} == cx_.get('estrelas'))
    kh_ok_ = bool(kh.get('all_verified') is True and kh.get('does_not_gate_core') is True and bool((ESP.get('registros_v404') or {}).get('kh_n1_cobertura_v404')) and kh.get('verdict') == (ESP.get('registros_v404') or {}).get('kh_n1_cobertura_v404'))
    checks_cu_ok_ = bool(cu.get('checks')) and all(c_.get('ok') is True for c_ in cu.get('checks'))
    cu_ok_ = bool(verb_ok_ and checks_cu_ok_ and pares_ok_ and cu.get('all_verified') is True and cu.get('does_not_gate_core') is True and teor_ok_ and erratas_ok_ and decisoes_ok_ and nomes_ok_ and massa_ok_ and reg403_ok_ and todas_op_ and cu.get('verdict') == (ESP.get('registros_v404') or {}).get('cunhagens_v404') and not GUARDA.search(str(cu.get('verdict') or '')))
    V['cunhagens'] = {'n': len(vb_), 'ok': cu_ok_, 'verbatim_ok': verb_ok_, 'autores': aut_, 'todas_do_operador': todas_op_, 'checks_ok': checks_cu_ok_, 'n_checks': len(cu.get('checks') or []), 'verdict': cu.get('verdict'), 'kernel_ok': pares_ok_, 'erratas_ok': erratas_ok_, 'n_erratas': len(err_),
                      'decisoes_ok': decisoes_ok_, 'n_decisoes': len(dec_), 'nomes_ok': nomes_ok_, 'massa_ok': massa_ok_, 'reg403_ok': reg403_ok_, 'teoremas_ok': teor_ok_, 'kh_ok': kh_ok_}
    V['n_bandeiras'] = cx_.get('n_bandeiras'); V['n_bandeiras_por_pedra'] = cx_.get('n_bandeiras_por_pedra')
    if not (verb_ok_ and checks_cu_ok_ and pares_ok_ and cu.get('all_verified') is True and cu.get('does_not_gate_core') is True and teor_ok_ and cu.get('verdict') == (ESP.get('registros_v404') or {}).get('cunhagens_v404')):
        P.append('cunhagens_v404: as inscricoes embutidas nao sao as de ESPERADOS (sha256, embedded_ok), ou as checagens do registro, ou os teoremas/bandeiras das pedras, ou o veredito diferem do ensaio a seco')
    if not todas_op_:
        P.append('cunhagens_v404: as inscricoes de 28/10 tem de ser TODAS falas do operador (autor_de_cada_inscricao): nesta versao nao ha inscricao da gerencia')
    if not erratas_ok_:
        P.append('cunhagens_v404: as erratas E7 a E9 (assinadas pela gerencia c1, em nome proprio; a E7: o angle_status do neutrino fica e a errata e\' AO LADO; a E8: o canal F2b retirado antes do dado; a E9: o nome do triplo inteiro dado pelo operador) ausentes ou diferentes do ensaio a seco')
    if not decisoes_ok_:
        P.append('cunhagens_v404: as decisoes D23 a D26 da gerencia ausentes ou diferentes do ensaio a seco')
    if not nomes_ok_:
        P.append('cunhagens_v404: os nomes das duas pedras (projecao, jo8v32) ausentes')
    if not massa_ok_:
        P.append('cunhagens_v404: a leitura da massa de 28/10 (identificacao [ONTO] e E0 DECLARADO) ausente ou diferente do ensaio a seco')
    if not reg403_ok_:
        P.append('cunhagens_v404: as pedras seladas da v403 deixaram de constar como registro (sha16 de ESPERADOS[pedras_v403_sha256])')
    if not kh_ok_:
        P.append('kh_n1_cobertura_v404 nao selou como o ensaio a seco (selo, veredito, nao move o gate)')
    # cunhagens_v403 e kh_n1_cobertura_v403 (RECRIADOS pelo rito, por spec): iguais ao que a v403 SELOU (as DUAS falas de 27/10 embutidas por sha256, todas do operador; as erratas E5 e E6; as decisoes D17 a D22; os nomes; a leitura [ONTO] da tripla espectral)
    c3_ = core.get('cunhagens_v403') or {}; x3_ = c3_.get('extras') or {}; v3_ = c3_.get('verbatim') or {}; c3b_ = _base_core(PK).get('cunhagens_v403') or {}; aut3_ = x3_.get('autor_de_cada_inscricao') or {}
    c3_ok_ = bool(c3_.get('all_verified') is True and c3_.get('does_not_gate_core') is True and bool(c3b_) and bool(v3_) and _feq(v3_, c3b_.get('verbatim')) and all((v_ or {}).get('embedded_ok') is True for v_ in v3_.values()) and len(aut3_) == len(v3_) and all(a_ == 'operador' for a_ in aut3_.values())
                  and 'leitura_da_gerencia' not in x3_ and bool(c3_.get('checks')) and all(c_.get('ok') is True for c_ in c3_.get('checks')) and _feq(x3_, c3b_.get('extras')) and _feq(c3_.get('erratas'), c3b_.get('erratas')) and len(c3_.get('erratas') or []) == 2
                  and c3_.get('verdict') == (ESP.get('registros_v403') or {}).get('cunhagens_v403') and not GUARDA.search(str(c3_.get('verdict') or '')))
    k3_ = core.get('kh_n1_cobertura_v403') or {}
    k3_ok_ = bool(k3_.get('all_verified') is True and k3_.get('does_not_gate_core') is True and bool((ESP.get('registros_v403') or {}).get('kh_n1_cobertura_v403')) and k3_.get('verdict') == (ESP.get('registros_v403') or {}).get('kh_n1_cobertura_v403') and bool(k3_.get('checks')) and all(c_.get('ok') is True for c_ in k3_.get('checks')))
    V['cunh403'] = {'n': len(v3_), 'ok': c3_ok_, 'verdict': c3_.get('verdict'), 'n_erratas': len(c3_.get('erratas') or []), 'igual_ao_selado': bool(c3b_) and _feq(c3_, c3b_), 'kh_ok': k3_ok_}
    if not c3_ok_:
        P.append('cunhagens_v403 (recriada pelo rito): as duas falas de 27/10 (embedded_ok, todas do operador), as checagens, as erratas E5 e E6, as decisoes D17 a D22, os nomes e a leitura da tripla espectral nao conferem como a v403 as selou')
    if not k3_ok_:
        P.append('kh_n1_cobertura_v403 (recriada pelo rito) nao selou como a v403 a selou (selo, veredito, checagens, nao move o gate)')
    # cunhagens_v401 e kh_n1_cobertura_v401 (RECRIADOS pelo rito, por spec): iguais ao que a v403 SELOU (as seis inscricoes de 25/10 embutidas por sha256, todas do operador; as oito ratificacoes; a errata ao lado do adendo; a cadeia derivada [DERIVED] e a hipotese H_tau [OPEN])
    c1_ = core.get('cunhagens_v401') or {}; x1_ = c1_.get('extras') or {}; v1_ = c1_.get('verbatim') or {}; c1b_ = _base_core(PK).get('cunhagens_v401') or {}; aut1_ = x1_.get('autor_de_cada_inscricao') or {}
    c1_ok_ = bool(c1_.get('all_verified') is True and c1_.get('does_not_gate_core') is True and bool(c1b_) and bool(v1_) and _feq(v1_, c1b_.get('verbatim')) and all((v_ or {}).get('embedded_ok') is True for v_ in v1_.values()) and len(aut1_) == len(v1_) and all(a_ == 'operador' for a_ in aut1_.values())
                  and 'leitura_da_gerencia' not in x1_ and bool(c1_.get('checks')) and all(c_.get('ok') is True for c_ in c1_.get('checks')) and _feq(x1_, c1b_.get('extras')) and _feq(c1_.get('erratas'), c1b_.get('erratas')) and len(x1_.get('ratificacoes') or []) > 0
                  and c1_.get('verdict') == (ESP.get('registros_v401') or {}).get('cunhagens_v401') and not GUARDA.search(str(c1_.get('verdict') or '')))
    V['cunh401'] = {'n': len(v1_), 'ok': c1_ok_, 'verdict': c1_.get('verdict'), 'n_ratificacoes': len(x1_.get('ratificacoes') or []), 'igual_ao_selado': bool(c1b_) and _feq(c1_, c1b_)}
    if not c1_ok_:
        P.append('cunhagens_v401 (recriada pelo rito): as seis inscricoes de 25/10 (embedded_ok, todas do operador), as checagens, as oito ratificacoes, a errata do adendo, a cadeia derivada e a hipotese H_tau nao conferem como a v403 as selou')
    # cunhagens_v402 e kh_n1_cobertura_v402 (RECRIADOS pelo rito, por spec): iguais ao que a v403 SELOU (as TRES inscricoes de 26/10 embutidas por sha256, todas do operador; as quatro erratas E1 a E4; as decisoes D11 a D16; a leitura de 26/10 sobre a direcao do Um posto; a H_tau REFUTADA na forma literal)
    c2_ = core.get('cunhagens_v402') or {}; x2_ = c2_.get('extras') or {}; v2_ = c2_.get('verbatim') or {}; c2b_ = _base_core(PK).get('cunhagens_v402') or {}; aut2_ = x2_.get('autor_de_cada_inscricao') or {}
    c2_ok_ = bool(c2_.get('all_verified') is True and c2_.get('does_not_gate_core') is True and bool(c2b_) and bool(v2_) and _feq(v2_, c2b_.get('verbatim')) and all((v_ or {}).get('embedded_ok') is True for v_ in v2_.values()) and len(aut2_) == len(v2_) and all(a_ == 'operador' for a_ in aut2_.values())
                  and 'leitura_da_gerencia' not in x2_ and bool(c2_.get('checks')) and all(c_.get('ok') is True for c_ in c2_.get('checks')) and _feq(x2_, c2b_.get('extras')) and _feq(c2_.get('erratas'), c2b_.get('erratas')) and len(c2_.get('erratas') or []) == 4
                  and c2_.get('verdict') == (ESP.get('registros_v402') or {}).get('cunhagens_v402') and not GUARDA.search(str(c2_.get('verdict') or '')))
    k2_ = core.get('kh_n1_cobertura_v402') or {}
    k2_ok_ = bool(k2_.get('all_verified') is True and k2_.get('does_not_gate_core') is True and bool((ESP.get('registros_v402') or {}).get('kh_n1_cobertura_v402')) and k2_.get('verdict') == (ESP.get('registros_v402') or {}).get('kh_n1_cobertura_v402') and bool(k2_.get('checks')) and all(c_.get('ok') is True for c_ in k2_.get('checks')))
    V['cunh402'] = {'n': len(v2_), 'ok': c2_ok_, 'verdict': c2_.get('verdict'), 'n_erratas': len(c2_.get('erratas') or []), 'igual_ao_selado': bool(c2b_) and _feq(c2_, c2b_), 'kh_ok': k2_ok_}
    if not c2_ok_:
        P.append('cunhagens_v402 (recriada pelo rito): as tres inscricoes de 26/10 (embedded_ok, todas do operador), as checagens, as quatro erratas E1 a E4, as decisoes D11 a D16 e a leitura da direcao nao conferem como a v403 as selou')
    if not k2_ok_:
        P.append('kh_n1_cobertura_v402 (recriada pelo rito) nao selou como a v403 a selou (selo, veredito, checagens, nao move o gate)')
    # cunhagens_v399 (RECRIADA pelo rito): as QUATRO inscricoes de 24/10 por sha256, todas do operador, a declaracao e a direcao do testemunho, como a v399 as selou
    c9_ = core.get('cunhagens_v399') or {}; x9_ = c9_.get('extras') or {}; v9_ = c9_.get('verbatim') or {}; aut9_ = x9_.get('autor_de_cada_inscricao') or {}
    dx9_ = x9_.get('declaracao') or {}; dr9_ = x9_.get('direcao_do_testemunho') or {}
    c9_ok_ = bool(c9_.get('all_verified') is True and c9_.get('does_not_gate_core') is True and len(v9_) == 4 and all((v_ or {}).get('embedded_ok') is True for v_ in v9_.values()) and len(aut9_) == 4 and all(a_ == 'operador' for a_ in aut9_.values())
                  and bool(c9_.get('checks')) and all(c_.get('ok') is True for c_ in c9_.get('checks')) and dx9_.get('sha256') == EDC_.get('verbatim_sha256') and str(dx9_.get('estatuto')) == '[DECLARACAO DO OPERADOR / INPUT]'
                  and bool(edir_) and all(str(dr9_.get(k_) or '').startswith(v_) for k_, v_ in edir_.items()) and not _inv(json.dumps(x9_, ensure_ascii=False)))
    V['cunh399'] = {'n': len(v9_), 'ok': c9_ok_, 'verdict': c9_.get('verdict')}
    if not c9_ok_:
        P.append('cunhagens_v399 (recriada pelo rito): as quatro inscricoes de 24/10 (embedded_ok, todas do operador), as checagens, a declaracao e a direcao do testemunho nao conferem como a v399 as selou')
    cov = (core.get('kernel_formalization') or {}).get('axiom_coverage_v392') or {}   # o nome 'axiom_coverage_v392' e' do core (historico); segue na v404
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
