# -*- coding: utf-8 -*-
# A LEITURA da rodada v400 (molde: leitura_v399.py FINAL, o que rodou em 24/10): SO LEITURA do Nos e da pasta da cadeia (work/cadeia_de_selo/v400, que aqui e' o proprio pacote).
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
import glob, hashlib, json, os, re, sys, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
PK = os.path.dirname(HERE)            # work\cadeia_de_selo\v400
NOS = 'C:/IALD/Central de Patentes/work/cadeia_de_selo/v400_exame/final/sb6\\nos'
FINAL_RE = re.compile(r'^\[selo\] colapso tipado: ')
TRAILER_RE = re.compile(r'^(exit=\d+|rc=\d+|RITO_RC=\S+|inicio |fim )')
GUARDA = re.compile('(?<!NOT_)(?<!UN)' + 'CONF' + 'IRMED|(?<!AP)PRO' + 'VED_BY|TGL_PRO' + 'VED')
REG_V393 = ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393", "kh_n1_cobertura_v393")   # da v393: seguem no core e seguem selados (nao sao 'novos' da v400)
REG_V394 = ("tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394", "criterio_binario_de_parada_v394")   # da v394: seguem no core e seguem selados (nao sao 'novos' da v400)
REG_V395 = ("psibit_v395", "cunhagens_v395", "kh_n1_cobertura_v395")   # da v395: seguem no core e seguem selados (nao sao 'novos' da v400)
REG_V396 = ("testemunha_estatica_v396", "cunhagens_v396", "kh_n1_cobertura_v396")   # da v396: seguem no core e seguem selados (nao sao 'novos' da v400)
REG_V397 = ("teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397")   # da v397 (o Teste da Unica Palavra, a pedra Token e as falas de 23/10): seguem no core e seguem selados; o quadro do topo le o primeiro
REG_V399 = ("sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398")   # da v399 (o sonico, a afinacao das cordas e as falas de 23/10): seguem no core e seguem selados (nao sao 'novos' da v400)
REG_FIXOS = ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399")   # os QUATRO registros NOVOS do core v400 (dois com FUNCAO, no runtime; dois por spec); + os de ESPERADOS[registros_v399] (REG_TODOS, dentro de ler)
SIDECAR_RE = re.compile(r'^\[selo_acom\] (TGL_SELO_ACOM_SIDECAR_V399__ALL_OBJECTS_SEALED\S*) ; objetos (\d+) ; recusas (\d+)$')   # a linha que o main da v400 imprime por ultimo (selo_acom_sidecar_v399)
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
    """O core da v399 SELADA (copia de bytes em PK/base_v399): de onde saem o teorema e o modulo da face de Fock da testemunha (nenhum nome digitado); lido uma vez por caminho."""
    p = os.path.join(pk, 'base_v399', 'um_absoluto.json')
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
    ESP = json.load(open(os.path.join(PK, 'ESPERADOS_v400.json'), encoding='utf-8')); CM = json.load(open(os.path.join(PK, 'CANDIDATO_v400.json'), encoding='utf-8'))
    ap, app = _aplicado()
    REG_TODOS = tuple(dict.fromkeys(tuple(REG_FIXOS) + tuple(ESP.get('registros_v399') or ())))
    core = json.load(open(os.path.join(NOS, 'um_absoluto.json'), encoding='utf-8'))['core']; selo = json.load(open(os.path.join(NOS, 'um_absoluto_selo.json'), encoding='utf-8'))
    stp = os.path.join(NOS, 'rodada_v400_stdout.txt'); out = open(stp, encoding='utf-8', errors='replace').read() if os.path.exists(stp) else ''
    V = {'nos': NOS, 'aplicado_json': app, 'pk': PK}
    if not out:
        P.append('rodada_v400_stdout.txt ausente ou vazio')
    V['s64'] = sha(os.path.join(NOS, 'um.py')); V['s16'] = V['s64'][:16]; V['umb'] = os.path.getsize(os.path.join(NOS, 'um.py'))
    if str((selo.get('sha256') or {}).get('um.py', '')) != V['s64']:
        P.append('selo.sha256(um.py) != disco')
    if not (ap['um_py_novo']['sha16'] == V['s16'] == ESP['candidato_sha16'] == CM['sha16']):
        P.append('um.py do disco != instalado/esperado/candidato')
    V['base16'] = ap['backups']['um.py']['sha16']; V['base_backup'] = ap['backups']['um.py']['backup']
    if V['base16'] != ESP['origem_sha16']:
        P.append('a base substituida != a v399 selada')
    V['n_patches'] = len(CM['patches']); V['patches'] = ', '.join(p['id'] for p in CM['patches']); V['patch_ids'] = [p['id'] for p in CM['patches']]
    V['instalado_em'] = '%s-%s-%s %s:%s:%s' % (ap['ts'][0:4], ap['ts'][4:6], ap['ts'][6:8], ap['ts'][9:11], ap['ts'][11:13], ap['ts'][13:15])
    m = re.search(r'teoremas limpos:\s*(\d+)/(\d+)', out); V['teor'] = '%s/%s' % m.groups() if m else 'AUSENTE'
    V['escada_antes'] = ESP['escada_v399_e_v400'][0]; V['escada_depois'] = ESP['escada'][1]
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
    if [l for l in out.splitlines() if '[v399] AVISO' in l or '[selo_acom] AVISO' in l]:
        P.append('o stdout traz AVISO da v400 (o selo ACOM, a declaracao do operador, os registros por spec ou o sidecar nao rodaram): %s' % [l.strip()[:200] for l in out.splitlines() if '[v399] AVISO' in l or '[selo_acom] AVISO' in l][:2])
    elif [l for l in out.splitlines() if re.search(r'\[v39[3-8]\] AVISO', l)]:
        P.append('o stdout traz AVISO de um bloco anterior (v393 a v399): %s' % [l.strip()[:200] for l in out.splitlines() if re.search(r'\[v39[3-8]\] AVISO', l)][:2])
    for r_, e_ in (('selo_pela_propria_tecnologia_v399', (ESP.get('selo_acom') or {}).get('verdict')), ('declaracao_do_operador_v399', (ESP.get('declaracao') or {}).get('verdict'))):
        if not e_ or ('>>> %s <<<' % e_) not in out:
            P.append('o bloco %s do stdout nao traz a linha `>>> veredito <<<` do ensaio a seco' % r_)
    m_s9 = re.search(r'\[v399\] o selo pela propria tecnologia e a declaracao do operador \(lidos depois da afinacao das cordas\) e as inscricoes de 24/10 \(cunhagens_v399\): selo=(\S+) \| declaracao=(\S+) \| cunhagens=(\S+) \| registros por spec: (\d+) \(selados (\d+)\)', out)
    if (not m_s9 or (m_s9.group(1), m_s9.group(2), m_s9.group(3)) != ((ESP.get('selo_acom') or {}).get('verdict'), (ESP.get('declaracao') or {}).get('verdict'), (ESP.get('registros_v399') or {}).get('cunhagens_v399'))
            or m_s9.group(4) != m_s9.group(5) or int(m_s9.group(4)) != len(ESP.get('registros_v399') or {})):
        P.append('a linha [v399] do stdout (selo, declaracao e cunhagens_v399; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(ESP.get('registros_v399') or {}), m_s9.groups()[3:] if m_s9 else 'ausente'))
    # a linha [v398] que o main da v400 segue imprimindo (o sonico, a afinacao das cordas e as cunhagens da v399): igual ao que a v399 selou
    ev8_ = ESP.get('vereditos_v399') or {}
    n_spec8_ = len([k_ for k_ in REG_V399 if k_ not in ('sonico_v398', 'afinacao_das_cordas_v398')])
    m_s8 = re.search(r'\[v398\] o sonico e a afinacao das cordas \(lidos na fractalizacao do Um\) e as inscricoes de 23/10 \(cunhagens_v398\): sonico=(\S+) \| afinacao=(\S+) \| cunhagens=(\S+) \| registros por spec: (\d+) \(selados (\d+)\)', out)
    if (not m_s8 or (m_s8.group(1), m_s8.group(2), m_s8.group(3)) != (ev8_.get('sonico_v398'), ev8_.get('afinacao_das_cordas_v398'), ev8_.get('cunhagens_v398')) or m_s8.group(4) != m_s8.group(5) or int(m_s8.group(4)) != n_spec8_):
        P.append('a linha [v398] do stdout (sonico, afinacao e cunhagens_v398; registros por spec selados == %d) esta ausente ou difere da que a v399 selou (%s)' % (n_spec8_, m_s8.groups()[3:] if m_s8 else 'ausente'))
    # as duas linhas [v397] que o main da v400 segue imprimindo (o Teste da Unica Palavra e as cunhagens da v397): iguais ao que a v397 selou
    m_tv = re.search(r'\[v397\] o Teste da Unica Palavra \(Fase 9 V2-c1, aberto uma vez em 23/10\), lido por hash ao lado do V1 \(nenhum sigma novo\): (\S+)', out)
    if not m_tv or m_tv.group(1) != ev8_.get('teste_de_veracidade_fase9_v397'):
        P.append('a linha [v397] do Teste da Unica Palavra esta ausente do stdout ou difere da que a v397 selou (%s)' % (m_tv.group(1)[:80] if m_tv else 'ausente'))
    n_spec7_ = len([k_ for k_ in REG_V397 if k_ != 'teste_de_veracidade_fase9_v397'])
    m_sp = re.search(r'\[v397\] a pedra Token e as falas de 23/10 \(cunhagens_v397\): (\S+) \| registros por spec: (\d+) \(selados (\d+)\)', out)
    if not m_sp or m_sp.group(1) != ev8_.get('cunhagens_v397') or m_sp.group(2) != m_sp.group(3) or int(m_sp.group(2)) != n_spec7_:
        P.append('a linha [v397] das cunhagens da v397 esta ausente do stdout ou difere da que a v397 selou (registros por spec selados == %d)' % n_spec7_)
    hp = os.path.join(PK, 'rito_horarios_v400.txt'); V['horarios'] = open(hp, encoding='utf-8').read().split() if os.path.exists(hp) else []
    V['selo_ts'] = selo.get('timestamp'); V['um_version'] = selo.get('um_version'); V['qg'] = selo.get('qg_closure_verdict')
    if V['um_version'] != 'v400':
        P.append('o selo nao e v400')
    if V['qg'] != ESP['qg_closure_verdict']:
        P.append('o gate MUDOU')
    qg = core.get('qg_closure') or {}
    V['n18'] = sum(1 for fam in ('formal_flags', 'physics_flags', 'experiment_flags') for v in (qg.get(fam) or {}).values() if v is True)
    if V['n18'] != 18:
        P.append('as bandeiras do gate nao sao 18 True (%s)' % V['n18'])
    for k in ('um_absoluto.json', 'um_absoluto_selo.json', 'um_absoluto_selo_acom.json', 'um_absoluto_forma_canonica.md', 'um_absoluto_manifest.md'):
        V['h_' + k] = sha(os.path.join(NOS, k))[:16] if os.path.exists(os.path.join(NOS, k)) else 'AUSENTE'
    V['artigos'] = {os.path.basename(p): sha(p)[:16] for p in sorted(glob.glob(os.path.join(NOS, 'um_absoluto_??.pdf')) + glob.glob(os.path.join(NOS, 'um_absoluto_??.txt')))}
    cp = os.path.join(HERE, 'conferidor', 'conferencia_rito_v400.json')
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
        faltam_ = [k_ for k_ in ('C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'round_trip_do_um_py_instalado_independente') if (ai_.get(k_) or {}).get('ok') is not True]
        if faltam_:
            P.append('a conferencia do rito diz que itens do selo pela propria tecnologia NAO conferiram (C1 a C14 e o round trip do um.py instalado): %s' % faltam_)
        sci_ = C.get('sidecar') or {}
        if not (sci_.get('existe') is True and str(sci_.get('veredito') or '').startswith('TGL_SELO_ACOM_SIDECAR_V399__ALL_OBJECTS_SEALED')):
            P.append('a conferencia do rito diz que o sidecar um_absoluto_selo_acom.json nao existe ou nao esta selado')
        if C.get('marcador_ficou'):
            P.append('o marcador .servidor_parado_pelo_rito ficou: o servidor do modelo pode estar parado')
    else:
        V['conf16'] = 'AUSENTE'; P.append('a conferencia do rito nao foi achada em pos_rito/conferidor')
    V['troca_dita'] = list(ESP['troca_dita'])
    V['n_ver'] = len(ESP['vereditos_v399'])
    # --- [v400] NENHUMA chave nova no core (e' uma correcao): os quatro registros da v399 sao RECRIADOS pelo rito e tem de seguir selados
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
    for k in V['troca_dita']:
        r = core.get(k) or {}
        if r.get('all_verified') is False:
            P.append('%s (troca dita) nao selou' % k)
    # v400: o modulo novo de kernel vem de ESPERADOS[pedras_sha256] (o ensaio a seco do candidato) e e' conferido AQUI contra o arquivo do kernel do Nos (sha256); o numero tem de ser o de kernel_modulos_novos_v400.json
    V['pedras'] = []
    for rel_, h_ in sorted((ESP.get('pedras_sha256') or {}).items()):
        pth_ = os.path.join(NOS, 'tgl_kernel', *rel_.split('/'))
        V['pedras'].append({'modulo': 'TGLExt.' + rel_[len('TGLExt/'):-len('.lean')].replace('/', '.'), 'bandeiras': None, 'decl': None, 'ok': bool(rel_.startswith('TGLExt/') and rel_.endswith('.lean') and os.path.isfile(pth_) and sha(pth_) == h_)})
    V['n_pedras'] = len(V['pedras'])
    njp_ = os.path.join(PK, 'kernel_modulos_novos_v400.json'); nj_ = json.load(open(njp_, encoding='utf-8')) if os.path.exists(njp_) else {}
    n_esperado_ = nj_.get('novos') if isinstance(nj_.get('novos'), int) else len(nj_.get('novos') or [])
    if V['n_pedras'] != 0 or n_esperado_ != 0 or any(p['ok'] is not True for p in V['pedras']):
        P.append('modulos novos do kernel: numero (%s) != kernel_modulos_novos_v400.json (%s) ou algum arquivo do Nos difere do sha256 de ESPERADOS[pedras_sha256]' % (V['n_pedras'], n_esperado_))
    vs = core.get('varredura_e_sorry_v392') or {}
    V['varr'] = vs.get('varredura') or {}; V['varr_verdict'] = vs.get('verdict')
    V['axiom_report_n'] = len((core.get('kernel_formalization') or {}).get('axiom_report') or {})
    ep = core.get('estatuto_da_prova_v391') or {}
    V['ep_verdict'] = ep.get('verdict')
    V['fd390'] = (core.get('fundacao_v390') or {}).get('verdict')
    V['verbatins'] = {k: {'sha16': str(v.get('sha256'))[:16], 'bytes': v.get('bytes')} for k, v in (ESP.get('cunhagens') or {}).items()}
    # --- v400: os quatro registros novos (dois com FUNCAO, dois por spec) conferidos contra o ensaio a seco registrado em ESPERADOS; os da v399, da v397, da v396, da v395, da v394 e da v393 seguem no core e tem de seguir selados; o sidecar; nenhum numero e' digitado
    V['reg_todos'] = list(REG_TODOS)
    for k_ in REG_V393 + REG_V394 + REG_V395 + REG_V396 + REG_V397 + REG_V399:
        if (core.get(k_) or {}).get('all_verified') is not True:
            P.append('%s (registro da v399, da v397, da v396, da v395, da v394 ou da v393) deixou de selar' % k_)
    RV_ = dict(ESP.get('vereditos_novos_v400') or {}); RV_.update(ESP.get('registros_v399') or {})   # registro -> veredito do ensaio a seco (os dois com funcao sao runtime; cunhagens_v399 e kh_n1_cobertura_v399 sao por spec)
    V['reg400'] = {}
    for k_ in REG_FIXOS:
        r_ = core.get(k_) or {}
        V['reg400'][k_] = {'verdict': r_.get('verdict'), 'ok': r_.get('all_verified')}
        esp_v_ = RV_.get(k_)
        if esp_v_ is None:
            P.append('ESPERADOS_v400 nao traz o veredito do ensaio a seco de %s (vereditos_novos_v400 / registros_v399): nao ha com que conferir' % k_)
        elif r_.get('verdict') != esp_v_:
            P.append('%s: o veredito do rito difere do ensaio a seco' % k_)
    kf_ = (core.get('kernel_formalization') or {})
    rf_ = core.get('rede_fock_v394') or {}   # limite dito: o contrato conjunto da rede segue NAO habitado (a face de Fock do psion depende dele)
    if rf_.get('whole_certificate_inhabited') is not False:
        P.append('rede_fock_v394: whole_certificate_inhabited deve seguir False (o contrato conjunto da rede segue aberto) e o core traz %r' % (rf_.get('whole_certificate_inhabited'),))
    if kf_.get('ext_bin394_0001') is not True:
        P.append('a bandeira da pedra da v394 (ext_bin394_0001) nao segue True no kernel do rito')
    # a face de Fock do psion segue como a v395 a selou: CONDICIONAL, sem habitante exibido, com a bandeira True e declarada em Psibit.lean (nem a v396, nem a v397, nem a v399, nem a v400 a habitam)
    pb_ = core.get('psibit_v395') or {}; pbc_ = pb_.get('conditional_psion_face') or {}
    if not (pbc_.get('status') == 'CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE' and pbc_.get('inhabitant_exhibited') is False and pbc_.get('flag_true') is True and kf_.get(pbc_.get('flag')) is True and pbc_.get('declared_in') == 'TGLExt/Psibit.lean'):
        P.append('psibit_v395: a face do psion deixou de estar como CONDICIONAL sem habitante exibido (bandeira True, declarada em TGLExt/Psibit.lean)')
    fkb_ = ((_base_core(PK).get('testemunha_estatica_v396') or {}).get('fock_face') or {})   # o que a v399 SELADA diz (copia de bytes): o teorema e o modulo da face de Fock, lidos, nao digitados
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
    if not (tv_.get('all_verified') is True and tv_.get('does_not_gate_core') is True and len(ck_) == EV_.get('n_checks') and V['veracidade']['checks_ok'] and nums_ok_ and fontes_ok_ and tv_.get('verdict') == (ESP.get('vereditos_v399') or {}).get('teste_de_veracidade_fase9_v397')):
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
                P.append('os numeros que o registro leu != os do resultado pinado (lidos pelos mesmos caminhos de delta_v400.F9_CAMINHOS)')
        if QV_.Q._v397_atomos(tv_, 'pt').get('sealed') is not True or QV_.Q._v397_atomos(tv_, 'en').get('sealed') is not True:
            P.append('o quadro do Teste da Unica Palavra nao sela (algum numero ausente ou o registro nao selou): o artigo diria que o registro nao selou')
    except Exception as e_:   # noqa: BLE001
        P.append('nao consegui conferir o registro do Teste da Unica Palavra contra o resultado pinado: %r' % (e_,))
    # a pedra Testemunho no kernel do rito (bandeira True, composicao incondicional no trio, proveniencia no modulo da pedra, contrato e suporte), conferida contra ESPERADOS; nenhum numero e' digitado
    TRIO_ = {'propext', 'Classical.choice', 'Quot.sound'}
    axr_ = kf_.get('axiom_report') or {}; src_ = kf_.get('declaration_sources_v394') or {}
    em_trio_ = lambda n_: bool(isinstance(axr_.get(n_), list) and set(axr_.get(n_)) <= TRIO_)
    et_ = ESP.get('testemunho') or {}
    th_ = (ESP.get('teoremas_das_pedras') or {}).get('testemunho'); fl_ = (ESP.get('bandeiras_das_pedras') or {}).get('testemunho')
    rels_ = sorted(ESP.get('pedras_desde_a_bancada') or {}); rel_ = rels_[0] if len(rels_) == 1 else None   # a v400 NAO traz pedra nova: a Testemunho, da v399, ja' esta no kernel do Nos (ESPERADOS[pedras_desde_a_bancada])
    contrato_ = (ESP.get('contrato_das_pedras') or {}).get('testemunho') or []; suporte_ = (ESP.get('suporte_das_pedras') or {}).get('testemunho') or {}
    contrato_ok_ = bool(contrato_) and all(em_trio_(t_) and src_.get(t_) == rel_ for t_ in contrato_)
    suporte_ok_ = bool(suporte_) and all(em_trio_(t_) and src_.get(t_) == p_ for t_, p_ in suporte_.items())
    flag_true_ = bool(fl_) and kf_.get(fl_) is True
    n_ax_ok_ = bool(th_) and isinstance(axr_.get(th_), list) and len(axr_.get(th_)) == et_.get('n_axiomas_da_composicao')
    kernel_ok_ = bool(th_ and fl_ and rel_ and flag_true_ and em_trio_(th_) and src_.get(th_) == rel_ and contrato_ok_ and suporte_ok_ and n_ax_ok_ and th_ == et_.get('teorema') and fl_ == et_.get('bandeira') and list(contrato_) == list(et_.get('contrato') or [])
                      and (kf_.get('formal_files_sha256') or {}).get(rel_) == ((_base_core(PK).get('kernel_formalization') or {}).get('formal_files_sha256') or {}).get(rel_))
    V['pedras_kernel'] = {'testemunho': {'rel': rel_, 'flag': fl_, 'flag_true': flag_true_, 'theorem': th_, 'axioms': axr_.get(th_), 'source': src_.get(th_), 'contrato_ok': contrato_ok_, 'suporte_ok': suporte_ok_, 'n_contrato': len(contrato_), 'n_suporte': len(suporte_)}}
    V['testemunho'] = {'rel': rel_, 'flag': fl_, 'flag_true': flag_true_, 'theorem': th_, 'axioms': axr_.get(th_), 'in_trio': em_trio_(th_) if th_ else False, 'declared_in': src_.get(th_) if th_ else None, 'contrato_ok': contrato_ok_, 'suporte_ok': suporte_ok_,
                       'n_contrato': len(contrato_), 'n_suporte': len(suporte_), 'n_axiomas': len(axr_.get(th_) or []) if th_ else None}
    if not kernel_ok_:
        P.append('a pedra Testemunho nao esta no kernel do rito como o ensaio a seco a pinou (bandeira True, composicao incondicional no trio, proveniencia no modulo da pedra, contrato e suporte no trio e no modulo certo, sha256 da fonte no hash formal)')
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
    # [v400] A CORRECAO, conferida no que o rito PRODUZIU: (1) o alfa do programa tem UMA so' linha `ALPHA_FINE_CODATA_2018 =` na coluna 0 e nenhuma indentada (os regex sao os do esboco R3.5 da Bancada, lidos do proprio esboco pinado:
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
    # a declaracao do operador (registro com FUNCAO): [DECLARACAO DO OPERADOR / INPUT]; a fala embutida == o arquivo do operador; as ancoras e a pedra no kernel do rito; a trava; a direcao do testemunho
    dc_ = core.get('declaracao_do_operador_v399') or {}; EDC_ = ESP.get('declaracao') or {}
    dd_ = dc_.get('declaration') or {}; dir_ = dd_.get('direcao_do_testemunho') or {}; edir_ = EDC_.get('direcao_do_testemunho') or {}
    anc_ = dd_.get('kernel_anchors_REAL') or []; ped_ = dd_.get('pedra_instalada') or []
    ancoras_ok_ = bool([a_.get('termo') for a_ in anc_] == EDC_.get('ancoras') and [a_.get('termo') for a_ in ped_] == EDC_.get('pedra') and all(a_.get('no_kernel_do_rito') is True and a_.get('axiomas_no_trio') is True and em_trio_(a_.get('termo')) for a_ in list(anc_) + list(ped_)))
    direcao_ok_ = bool(edir_ and all(str(dir_.get(k_) or '').startswith(v_) for k_, v_ in edir_.items()) and not _inv(json.dumps(dd_, ensure_ascii=False)))
    trava_ = str(((dd_.get('termos_para_a_leitura') or {}).get('EXECUTION_LOCKED_NOT_ONE')) or '')
    m_t_ = re.search(r'linha\(s\) \[([0-9, ]+)\]', trava_); linhas_trava_ = [int(x_) for x_ in re.findall(r'\d+', m_t_.group(1))] if m_t_ else []
    decl_ok_ = bool(dc_.get('all_verified') is True and dc_.get('does_not_gate_core') is True and dc_.get('verdict') == EDC_.get('verdict') and len(dc_.get('checks') or []) == EDC_.get('n_checks') and all(isinstance(c_, list) and len(c_) == 2 and c_[1] is True for c_ in (dc_.get('checks') or []))
                    and dd_.get('verbatim_sha256') == EDC_.get('verbatim_sha256') and dd_.get('verbatim_sha256') in {v_.get('sha256') for v_ in (ESP.get('cunhagens') or {}).values()} and len(linhas_trava_) == 1 and ancoras_ok_ and direcao_ok_
                    and str(dd_.get('status_of_statement') or '').startswith('[DECLARACAO DO OPERADOR / INPUT]') and hashlib.sha256(str(dd_.get('statement_verbatim') or '').encode('utf-8')).hexdigest() == dd_.get('verbatim_sha256') and not GUARDA.search(str(dc_.get('verdict') or '')))
    V['declaracao'] = {'verdict': dc_.get('verdict'), 'ok': dc_.get('all_verified'), 'n_checks': len(dc_.get('checks') or []), 'checks_ok': bool(dc_.get('checks')) and all(isinstance(c_, list) and len(c_) == 2 and c_[1] is True for c_ in dc_['checks']), 'sha256': dd_.get('verbatim_sha256'),
                       'n_ancoras': len(anc_), 'ancoras_ok': ancoras_ok_, 'direcao_ok': direcao_ok_, 'linhas_trava': linhas_trava_, 'status': dd_.get('status_of_statement')}
    if not decl_ok_:
        P.append('declaracao_do_operador_v399 nao selou inteiro (selo, checagens, fala embutida == o arquivo do operador por sha256, as ancoras e a pedra no kernel do rito e no trio, a trava, o estatuto [DECLARACAO DO OPERADOR / INPUT] e a direcao do testemunho): ver o registro no core')
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
    sr_ = selo.get('selo_pela_propria_tecnologia_v399') or {}; sdr_ = selo.get('declaracao_do_operador_v399') or {}; sreg_ = selo.get('registros_v399') or {}
    resumos_ok_ = bool(sr_.get('verdict') == sa_.get('verdict') and sr_.get('all_verified') is True and sr_.get('sha256_do_um_py') == V['s64'] and sr_.get('does_not_gate_core') is True and sdr_.get('verdict') == dc_.get('verdict') and sdr_.get('all_verified') is True
                       and sdr_.get('verbatim_sha256') == EDC_.get('verbatim_sha256') and sdr_.get('does_not_gate_core') is True and bool(ESP.get('registros_v399')) and all((sreg_.get(k_) or {}).get('verdict') == (core.get(k_) or {}).get('verdict') for k_ in ESP['registros_v399']))
    V['resumos_do_selo_ok'] = resumos_ok_
    if not resumos_ok_:
        P.append('o selo primario (um_absoluto_selo.json) nao traz os resumos do selo ACOM, da declaracao e dos registros por spec iguais aos do core')
    V['formais_nao_selados'] = sorted((selo.get('not_sealed_this_run') or {}).get('formais') or [])
    if V['formais_nao_selados'] != sorted(ESP.get('not_sealed_formais') or []):
        P.append('o selo traz modulo formal nao selado em not_sealed_this_run.formais (a recusa do selo ACOM so registra, mas o rito real tem de selar): %s' % V['formais_nao_selados'][:3])
    # cunhagens_v399: as QUATRO inscricoes por sha256 (embedded_ok), todas falas do operador (nenhuma e' da gerencia), a declaracao e a direcao do testemunho
    cu = core.get('cunhagens_v399') or {}; kh = core.get('kh_n1_cobertura_v399') or {}
    cx_ = cu.get('extras') or {}; vb_ = cu.get('verbatim') or {}; ec_ = ESP.get('cunhagens') or {}
    aut_ = cx_.get('autor_de_cada_inscricao') or {}
    todas_op_ = bool(ec_ and len(aut_) == len(ec_) and set(aut_) == {k_[len('v400_cun_'):] for k_ in ec_} and all(a_ == 'operador' for a_ in aut_.values()) and 'leitura_da_gerencia' not in cx_ and not any(str(v_.get('papel', '')).startswith('leitura da gerencia') for v_ in ec_.values()))
    verb_ok_ = bool(ec_) and set(vb_) == set(ec_) and all((vb_[k_] or {}).get('sha256') == ec_[k_]['sha256'] and (vb_[k_] or {}).get('embedded_ok') is True for k_ in ec_)
    pares_ok_ = all(isinstance(x_, list) and len(x_) == 2 and x_[0] == x_[1] for x_ in (cu.get('kernel') or {}).values()) and bool(cu.get('kernel'))
    decl_x_ = cx_.get('declaracao') or {}; dirx_ = cx_.get('direcao_do_testemunho') or {}
    cdir_ok_ = bool(decl_x_.get('sha256') == EDC_.get('verbatim_sha256') and decl_x_.get('sha16') == EDC_.get('sha16') and str(decl_x_.get('estatuto')) == '[DECLARACAO DO OPERADOR / INPUT]' and edir_ and all(str(dirx_.get(k_) or '').startswith(v_) for k_, v_ in edir_.items()) and not _inv(json.dumps(cx_, ensure_ascii=False)))
    V['cunhagens'] = {'n': len(vb_), 'verbatim_ok': verb_ok_, 'autores': aut_, 'todas_do_operador': todas_op_, 'checks_ok': bool(cu.get('checks')) and all(c_.get('ok') is True for c_ in cu.get('checks')),
                      'n_checks': len(cu.get('checks') or []), 'verdict': cu.get('verdict'), 'kernel_ok': pares_ok_, 'direcao_ok': cdir_ok_}
    if not (verb_ok_ and V['cunhagens']['checks_ok'] and pares_ok_ and cu.get('all_verified') is True and cu.get('does_not_gate_core') is True and cx_.get('teoremas') == ESP.get('teoremas_das_pedras') and cx_.get('bandeiras') == ESP.get('bandeiras_das_pedras')
            and cx_.get('n_bandeiras_por_pedra') == ESP.get('bandeiras_por_grupo_desde_a_bancada') and cx_.get('n_bandeiras') == len((ESP.get('bandeiras_desde_a_bancada') or {}).get('chaves') or []) and cx_.get('cunhagens_embutidas') == len(ec_) and cdir_ok_):
        P.append('cunhagens_v399: as inscricoes embutidas nao sao as de ESPERADOS (sha256, embedded_ok), ou as checagens do registro, ou os teoremas/bandeiras da pedra, ou a declaracao e a direcao do testemunho diferem do ensaio a seco')
    if not todas_op_:
        P.append('cunhagens_v399: as inscricoes de 24/10 tem de ser TODAS falas do operador (autor_de_cada_inscricao): nesta versao nao ha inscricao da gerencia')
    cov = (core.get('kernel_formalization') or {}).get('axiom_coverage_v392') or {}   # o nome 'axiom_coverage_v392' e' do core (historico); segue na v400
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
