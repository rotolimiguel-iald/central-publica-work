# -*- coding: utf-8 -*-
# A LEITURA da rodada v398 (molde: leitura_v397.py FINAL, o que rodou em 23/10): SO LEITURA do Nos e da pasta da cadeia (work/cadeia_de_selo/v398, que aqui e' o proprio pacote).
# Devolve (V, PROBLEMAS); PROBLEMAS nao vazio => a cadeia PARA. Nenhum numero e' digitado: tudo sai dos JSON, do core, do selo e do stdout do rito.
# v398: os registros NOVOS do core sao sonico_v398 e afinacao_das_cordas_v398 (com FUNCAO, no runtime: lidos NA FRACTALIZACAO DO UM, logo depois da testemunha_estatica_v396; cada um LE do kernel do proprio rito a composicao incondicional da sua pedra,
# os termos que ela cita e as inscricoes de 23/10, e CONFERE um calculo) e cunhagens_v398 e kh_n1_cobertura_v398 (por spec; ESPERADOS[registros_v398]); os da v397 (teste_de_veracidade_fase9_v397, cunhagens_v397, kh_n1_cobertura_v397), os da v396, os da v395,
# os da v394 e os da v393 seguem no core e tem de seguir selados. Os modulos novos de kernel (TGLExt/Sonico.lean e TGLExt/AfinacaoDasCordas.lean) vem de ESPERADOS[pedras_sha256] e sao conferidos aqui contra os arquivos do kernel do Nos.
# A escada vem de ESPERADOS[escada_v397_e_v398] e ESPERADOS[escada]; a troca dita (so numeros) e' a de ESPERADOS[troca_dita]. sonico_v398 e afinacao_das_cordas_v398 sao conferidos por inteiro (veredito == o do ensaio a seco, checagens, NUMEROS == ESPERADOS:
# ln 2, exp(ln 2), a entropia do colapso em theta_M em nats e em oitavas; zeta(-1) = -1/12, zeta(-1, 1/2) = 1/24, D = 26, D = 10, d = 9; a hipotese MasslessFirstLevel segue KNOWN, a geometria OPEN, nada deriva cordas do axioma, o kappa do boost nao vem do core),
# e cada pedra e' conferida no kernel do rito (bandeira True, composicao no trio, modulo da pedra, contrato e suporte). cunhagens_v398: as SEIS inscricoes por sha256 (embedded_ok) e a sexta, e so' ela, ROTULADA como da gerencia (nunca fala do operador).
# O QUADRO «O Teste da Unica Palavra» (v397) segue selado e igual: o registro teste_de_veracidade_fase9_v397 == ESPERADOS e == o resultado pinado, o quadro sela nas duas linguas, e a conferencia do rito diz que ele segue no topo (artigo PT/EN e .md).
# A face de Fock do psion segue CONDICIONAL (psibit_v395 e testemunha_estatica_v396); as linhas `[v398]` e `[v397]` do stdout do rito dizem os vereditos e registros por spec selados == registros por spec; o AVISO da v398 (e de qualquer bloco v393 a v397) no stdout reprova.
# Diferencas para a v397: os registros novos sao DESCOBERTOS por comparacao com ESPERADOS[vereditos_v397]; V['sonico'], V['afinacao'], V['cunhagens'], V['pedras_kernel'], V['reg398'] e V['patch_ids'] sao os campos da v398.
import glob, hashlib, json, os, re, sys, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
PK = os.path.dirname(HERE)            # work\cadeia_de_selo\v398
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
FINAL_RE = re.compile(r'^\[selo\] colapso tipado: ')
TRAILER_RE = re.compile(r'^(exit=\d+|rc=\d+|RITO_RC=\S+|inicio |fim )')
GUARDA = re.compile('(?<!NOT_)(?<!UN)' + 'CONF' + 'IRMED|(?<!AP)PRO' + 'VED_BY|TGL_PRO' + 'VED')
REG_V393 = ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "cunhagens_regra_v393", "kh_n1_cobertura_v393")   # da v393: seguem no core e seguem selados (nao sao 'novos' da v398)
REG_V394 = ("tempo_frequencia_v394", "regra_quadratica_v394", "rede_fock_v394", "cunhagens_v394", "kh_n1_cobertura_v394", "criterio_binario_de_parada_v394")   # da v394: seguem no core e seguem selados (nao sao 'novos' da v398)
REG_V395 = ("psibit_v395", "cunhagens_v395", "kh_n1_cobertura_v395")   # da v395: seguem no core e seguem selados (nao sao 'novos' da v398)
REG_V396 = ("testemunha_estatica_v396", "cunhagens_v396", "kh_n1_cobertura_v396")   # da v396: seguem no core e seguem selados (nao sao 'novos' da v398)
REG_V397 = ("teste_de_veracidade_fase9_v397", "cunhagens_v397", "kh_n1_cobertura_v397")   # da v397 (o Teste da Unica Palavra, a pedra Token e as falas de 23/10): seguem no core e seguem selados (nao sao 'novos' da v398); o quadro do topo le o primeiro
REG_FIXOS = ("sonico_v398", "afinacao_das_cordas_v398", "cunhagens_v398", "kh_n1_cobertura_v398")   # os QUATRO registros NOVOS do core v398 (dois com FUNCAO, no runtime; dois por spec); + os de ESPERADOS[registros_v398] (REG_TODOS, dentro de ler)
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


_BASE_CORE = {}


def _base_core(pk):
    """O core da v397 SELADA (copia de bytes em PK/base_v397): de onde saem o teorema e o modulo da face de Fock da testemunha (nenhum nome digitado); lido uma vez por caminho."""
    p = os.path.join(pk, 'base_v397', 'um_absoluto.json')
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
    ESP = json.load(open(os.path.join(PK, 'ESPERADOS_v398.json'), encoding='utf-8')); CM = json.load(open(os.path.join(PK, 'CANDIDATO_v398.json'), encoding='utf-8'))
    ap, app = _aplicado()
    REG_TODOS = tuple(dict.fromkeys(tuple(REG_FIXOS) + tuple(ESP.get('registros_v398') or ())))
    core = json.load(open(os.path.join(NOS, 'um_absoluto.json'), encoding='utf-8'))['core']; selo = json.load(open(os.path.join(NOS, 'um_absoluto_selo.json'), encoding='utf-8'))
    stp = os.path.join(NOS, 'rodada_v398_stdout.txt'); out = open(stp, encoding='utf-8', errors='replace').read() if os.path.exists(stp) else ''
    V = {'nos': NOS, 'aplicado_json': app, 'pk': PK}
    if not out:
        P.append('rodada_v398_stdout.txt ausente ou vazio')
    V['s64'] = sha(os.path.join(NOS, 'um.py')); V['s16'] = V['s64'][:16]; V['umb'] = os.path.getsize(os.path.join(NOS, 'um.py'))
    if str((selo.get('sha256') or {}).get('um.py', '')) != V['s64']:
        P.append('selo.sha256(um.py) != disco')
    if not (ap['um_py_novo']['sha16'] == V['s16'] == ESP['candidato_sha16'] == CM['sha16']):
        P.append('um.py do disco != instalado/esperado/candidato')
    V['base16'] = ap['backups']['um.py']['sha16']; V['base_backup'] = ap['backups']['um.py']['backup']
    if V['base16'] != ESP['origem_sha16']:
        P.append('a base substituida != a v397 selada')
    V['n_patches'] = len(CM['patches']); V['patches'] = ', '.join(p['id'] for p in CM['patches']); V['patch_ids'] = [p['id'] for p in CM['patches']]
    V['instalado_em'] = '%s-%s-%s %s:%s:%s' % (ap['ts'][0:4], ap['ts'][4:6], ap['ts'][6:8], ap['ts'][9:11], ap['ts'][11:13], ap['ts'][13:15])
    m = re.search(r'teoremas limpos:\s*(\d+)/(\d+)', out); V['teor'] = '%s/%s' % m.groups() if m else 'AUSENTE'
    V['escada_antes'] = ESP['escada_v397_e_v398'][0]; V['escada_depois'] = ESP['escada'][1]
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
    sujo = [l for l in out.splitlines() if 'Traceback' in l or l.startswith('[selo] AVISO')]
    if sujo:
        P.append('stdout com Traceback/AVISO: %s' % sujo[:3])
    linhas = [l for l in out.splitlines() if l.strip() and not TRAILER_RE.match(l.strip())]
    if not linhas or not FINAL_RE.match(linhas[-1]):
        P.append('a ultima linha do stdout nao e a linha final do rito')
    mrc = re.findall(r'^RITO_RC=(\S+)', out, flags=re.M); V['rc'] = mrc[-1] if mrc else 'NAO_LIDO'
    if V['rc'] != '0':
        P.append('rc do rito nao lido como 0 (%s)' % V['rc'])
    if len([l for l in out.splitlines() if '[v398]' in l]) < 1:
        P.append('o stdout nao tem a linha [v398]')
    if [l for l in out.splitlines() if '[v398] AVISO' in l]:
        P.append('o stdout traz AVISO da v398 (o sonico, a afinacao das cordas ou os registros por spec nao rodaram): %s' % [l.strip()[:200] for l in out.splitlines() if '[v398] AVISO' in l][:2])
    elif [l for l in out.splitlines() if re.search(r'\[v39[3-7]\] AVISO', l)]:
        P.append('o stdout traz AVISO de um bloco anterior (v393 a v397): %s' % [l.strip()[:200] for l in out.splitlines() if re.search(r'\[v39[3-7]\] AVISO', l)][:2])
    for k_, r_ in (('sonico', 'sonico_v398'), ('afinacao', 'afinacao_das_cordas_v398')):
        ver_ = (ESP.get(k_) or {}).get('verdict')
        if not ver_ or ('>>> %s <<<' % ver_) not in out:
            P.append('o bloco %s do stdout nao traz a linha `>>> veredito <<<` do ensaio a seco' % r_)
    m_s8 = re.search(r'\[v398\] o sonico e a afinacao das cordas \(lidos na fractalizacao do Um\) e as inscricoes de 23/10 \(cunhagens_v398\): sonico=(\S+) \| afinacao=(\S+) \| cunhagens=(\S+) \| registros por spec: (\d+) \(selados (\d+)\)', out)
    if (not m_s8 or (m_s8.group(1), m_s8.group(2), m_s8.group(3)) != ((ESP.get('sonico') or {}).get('verdict'), (ESP.get('afinacao') or {}).get('verdict'), (ESP.get('registros_v398') or {}).get('cunhagens_v398'))
            or m_s8.group(4) != m_s8.group(5) or int(m_s8.group(4)) != len(ESP.get('registros_v398') or {})):
        P.append('a linha [v398] do stdout (sonico, afinacao e cunhagens_v398; registros por spec selados == %d) esta ausente ou difere do ensaio a seco (%s)' % (len(ESP.get('registros_v398') or {}), m_s8.groups()[3:] if m_s8 else 'ausente'))
    # as duas linhas [v397] que o main da v398 segue imprimindo (o Teste da Unica Palavra e as cunhagens da v397): iguais ao que a v397 selou
    m_tv = re.search(r'\[v397\] o Teste da Unica Palavra \(Fase 9 V2-c1, aberto uma vez em 23/10\), lido por hash ao lado do V1 \(nenhum sigma novo\): (\S+)', out)
    if not m_tv or m_tv.group(1) != (ESP.get('vereditos_v397') or {}).get('teste_de_veracidade_fase9_v397'):
        P.append('a linha [v397] do Teste da Unica Palavra esta ausente do stdout ou difere da que a v397 selou (%s)' % (m_tv.group(1)[:80] if m_tv else 'ausente'))
    n_spec7_ = len([k_ for k_ in REG_V397 if k_ != 'teste_de_veracidade_fase9_v397'])
    m_sp = re.search(r'\[v397\] a pedra Token e as falas de 23/10 \(cunhagens_v397\): (\S+) \| registros por spec: (\d+) \(selados (\d+)\)', out)
    if not m_sp or m_sp.group(1) != (ESP.get('vereditos_v397') or {}).get('cunhagens_v397') or m_sp.group(2) != m_sp.group(3) or int(m_sp.group(2)) != n_spec7_:
        P.append('a linha [v397] das cunhagens da v397 esta ausente do stdout ou difere da que a v397 selou (registros por spec selados == %d)' % n_spec7_)
    hp = os.path.join(PK, 'rito_horarios_v398.txt'); V['horarios'] = open(hp, encoding='utf-8').read().split() if os.path.exists(hp) else []
    V['selo_ts'] = selo.get('timestamp'); V['um_version'] = selo.get('um_version'); V['qg'] = selo.get('qg_closure_verdict')
    if V['um_version'] != 'v398':
        P.append('o selo nao e v398')
    if V['qg'] != ESP['qg_closure_verdict']:
        P.append('o gate MUDOU')
    qg = core.get('qg_closure') or {}
    V['n18'] = sum(1 for fam in ('formal_flags', 'physics_flags', 'experiment_flags') for v in (qg.get(fam) or {}).values() if v is True)
    if V['n18'] != 18:
        P.append('as bandeiras do gate nao sao 18 True (%s)' % V['n18'])
    for k in ('um_absoluto.json', 'um_absoluto_selo.json', 'um_absoluto_forma_canonica.md', 'um_absoluto_manifest.md'):
        V['h_' + k] = sha(os.path.join(NOS, k))[:16] if os.path.exists(os.path.join(NOS, k)) else 'AUSENTE'
    V['artigos'] = {os.path.basename(p): sha(p)[:16] for p in sorted(glob.glob(os.path.join(NOS, 'um_absoluto_??.pdf')) + glob.glob(os.path.join(NOS, 'um_absoluto_??.txt')))}
    cp = os.path.join(HERE, 'conferidor', 'conferencia_rito_v398.json')
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
        if C.get('marcador_ficou'):
            P.append('o marcador .servidor_parado_pelo_rito ficou: o servidor do modelo pode estar parado')
    else:
        V['conf16'] = 'AUSENTE'; P.append('a conferencia do rito nao foi achada em pos_rito/conferidor')
    V['troca_dita'] = list(ESP['troca_dita'])
    V['n_ver'] = len(ESP['vereditos_v397'])
    # --- os registros novos: descobertos por comparacao com o que a v397 ja tinha
    novos = []
    for k, r in core.items():
        if isinstance(r, dict) and 'verdict' in r and k not in ESP['vereditos_v397']:
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
    for k in V['troca_dita']:
        r = core.get(k) or {}
        if r.get('all_verified') is False:
            P.append('%s (troca dita) nao selou' % k)
    # v398: o modulo novo de kernel vem de ESPERADOS[pedras_sha256] (o ensaio a seco do candidato) e e' conferido AQUI contra o arquivo do kernel do Nos (sha256); o numero tem de ser o de kernel_modulos_novos_v398.json
    V['pedras'] = []
    for rel_, h_ in sorted((ESP.get('pedras_sha256') or {}).items()):
        pth_ = os.path.join(NOS, 'tgl_kernel', *rel_.split('/'))
        V['pedras'].append({'modulo': 'TGLExt.' + rel_[len('TGLExt/'):-len('.lean')].replace('/', '.'), 'bandeiras': None, 'decl': None, 'ok': bool(rel_.startswith('TGLExt/') and rel_.endswith('.lean') and os.path.isfile(pth_) and sha(pth_) == h_)})
    V['n_pedras'] = len(V['pedras'])
    njp_ = os.path.join(PK, 'kernel_modulos_novos_v398.json'); nj_ = json.load(open(njp_, encoding='utf-8')) if os.path.exists(njp_) else {}
    n_esperado_ = nj_.get('novos') if isinstance(nj_.get('novos'), int) else len(nj_.get('novos') or [])
    if not V['n_pedras'] or V['n_pedras'] != n_esperado_ or any(p['ok'] is not True for p in V['pedras']):
        P.append('modulos novos do kernel: numero (%s) != kernel_modulos_novos_v398.json (%s) ou algum arquivo do Nos difere do sha256 de ESPERADOS[pedras_sha256]' % (V['n_pedras'], n_esperado_))
    vs = core.get('varredura_e_sorry_v392') or {}
    V['varr'] = vs.get('varredura') or {}; V['varr_verdict'] = vs.get('verdict')
    V['axiom_report_n'] = len((core.get('kernel_formalization') or {}).get('axiom_report') or {})
    ep = core.get('estatuto_da_prova_v391') or {}
    V['ep_verdict'] = ep.get('verdict')
    V['fd390'] = (core.get('fundacao_v390') or {}).get('verdict')
    V['verbatins'] = {k: {'sha16': str(v.get('sha256'))[:16], 'bytes': v.get('bytes')} for k, v in (ESP.get('cunhagens') or {}).items()}
    # --- v398: os quatro registros novos conferidos contra o ensaio a seco registrado em ESPERADOS, e os da v397, da v396, da v395, da v394 e da v393, que seguem no core e tem de seguir selados; nenhum numero e' digitado
    V['reg_todos'] = list(REG_TODOS)
    for k_ in REG_V393 + REG_V394 + REG_V395 + REG_V396 + REG_V397:
        if (core.get(k_) or {}).get('all_verified') is not True:
            P.append('%s (registro da v397, da v396, da v395, da v394 ou da v393) deixou de selar' % k_)
    RV_ = dict(ESP.get('vereditos_novos_v398') or {}); RV_.update(ESP.get('registros_v398') or {})   # registro -> veredito do ensaio a seco (sonico_v398 e afinacao_das_cordas_v398 sao runtime, com funcao; cunhagens_v398 e kh_n1_cobertura_v398 sao por spec)
    V['reg398'] = {}
    for k_ in REG_FIXOS:
        r_ = core.get(k_) or {}
        V['reg398'][k_] = {'verdict': r_.get('verdict'), 'ok': r_.get('all_verified')}
        esp_v_ = RV_.get(k_)
        if esp_v_ is None:
            P.append('ESPERADOS_v398 nao traz o veredito do ensaio a seco de %s (vereditos_novos_v398 / registros_v398): nao ha com que conferir' % k_)
        elif r_.get('verdict') != esp_v_:
            P.append('%s: o veredito do rito difere do ensaio a seco' % k_)
    kf_ = (core.get('kernel_formalization') or {})
    rf_ = core.get('rede_fock_v394') or {}   # limite dito: o contrato conjunto da rede segue NAO habitado (a face de Fock do psion depende dele)
    if rf_.get('whole_certificate_inhabited') is not False:
        P.append('rede_fock_v394: whole_certificate_inhabited deve seguir False (o contrato conjunto da rede segue aberto) e o core traz %r' % (rf_.get('whole_certificate_inhabited'),))
    if kf_.get('ext_bin394_0001') is not True:
        P.append('a bandeira da pedra da v394 (ext_bin394_0001) nao segue True no kernel do rito')
    # a face de Fock do psion segue como a v395 a selou: CONDICIONAL, sem habitante exibido, com a bandeira True e declarada em Psibit.lean (nem a v396, nem a v397, nem a v398 a habitam)
    pb_ = core.get('psibit_v395') or {}; pbc_ = pb_.get('conditional_psion_face') or {}
    if not (pbc_.get('status') == 'CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE' and pbc_.get('inhabitant_exhibited') is False and pbc_.get('flag_true') is True and kf_.get(pbc_.get('flag')) is True and pbc_.get('declared_in') == 'TGLExt/Psibit.lean'):
        P.append('psibit_v395: a face do psion deixou de estar como CONDICIONAL sem habitante exibido (bandeira True, declarada em TGLExt/Psibit.lean)')
    fkb_ = ((_base_core(PK).get('testemunha_estatica_v396') or {}).get('fock_face') or {})   # o que a v397 SELADA diz (copia de bytes): o teorema e o modulo da face de Fock, lidos, nao digitados
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
    if not (tv_.get('all_verified') is True and tv_.get('does_not_gate_core') is True and len(ck_) == EV_.get('n_checks') and V['veracidade']['checks_ok'] and nums_ok_ and fontes_ok_ and tv_.get('verdict') == (ESP.get('vereditos_v397') or {}).get('teste_de_veracidade_fase9_v397')):
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
                P.append('os numeros que o registro leu != os do resultado pinado (lidos pelos mesmos caminhos de delta_v398.F9_CAMINHOS)')
        if QV_.Q._v397_atomos(tv_, 'pt').get('sealed') is not True or QV_.Q._v397_atomos(tv_, 'en').get('sealed') is not True:
            P.append('o quadro do Teste da Unica Palavra nao sela (algum numero ausente ou o registro nao selou): o artigo diria que o registro nao selou')
    except Exception as e_:   # noqa: BLE001
        P.append('nao consegui conferir o registro do Teste da Unica Palavra contra o resultado pinado: %r' % (e_,))
    # as DUAS pedras no kernel do rito e os dois registros com funcao, conferidos contra o ensaio a seco (ESPERADOS[sonico] e ESPERADOS[afinacao]); nenhum numero e' digitado
    TRIO_ = {'propext', 'Classical.choice', 'Quot.sound'}
    axr_ = kf_.get('axiom_report') or {}; src_ = kf_.get('declaration_sources_v394') or {}
    em_trio_ = lambda n_: bool(isinstance(axr_.get(n_), list) and set(axr_.get(n_)) <= TRIO_)
    NOME_PEDRA_ = {'sonico': 'Sonico', 'afinacao': 'AfinacaoDasCordas'}
    V['pedras_kernel'] = {}
    for key_, rn_ in (('sonico', 'sonico_v398'), ('afinacao', 'afinacao_das_cordas_v398')):
        ek_ = ESP.get(key_) or {}; rec_ = core.get(rn_) or {}
        th_ = (ESP.get('teoremas_das_pedras') or {}).get(key_); fl_ = (ESP.get('bandeiras_das_pedras') or {}).get(key_); rel_ = (ek_.get('unconditional') or {}).get('declared_in')
        contrato_ = (ESP.get('contrato_das_pedras') or {}).get(key_) or []; suporte_ = (ESP.get('suporte_das_pedras') or {}).get(key_) or {}
        un_ = rec_.get('unconditional') or {}; mec_ = rec_.get('mechanics') or {}; vals_ = rec_.get('values') or {}
        contrato_ok_ = bool(contrato_) and all(em_trio_(t_) and src_.get(t_) == rel_ for t_ in contrato_)
        suporte_ok_ = bool(suporte_) and all(em_trio_(t_) and src_.get(t_) == p_ for t_, p_ in suporte_.items())
        flag_true_ = bool(fl_) and kf_.get(fl_) is True
        kernel_ok_ = bool(th_ and fl_ and rel_ and flag_true_ and em_trio_(th_) and src_.get(th_) == rel_ and contrato_ok_ and suporte_ok_ and un_.get('in_kernel') is True and un_.get('flag_true') is True and un_.get('theorem') == th_
                          and un_.get('flag') == fl_ and rec_.get('exact_ladder') is True and rec_.get('embedded_source_ok') is True and all(v_ is True for v_ in (rec_.get('support_theorems') or {}).values()) and bool(rec_.get('support_theorems')))
        checks_ok_ = bool(mec_.get('checks')) and mec_.get('passed') is True and mec_.get('n_checks') == ek_.get('n_checks') and all(c_.get('ok') is True for c_ in mec_.get('checks'))
        values_ok_ = bool(ek_.get('values')) and _feq(vals_, ek_.get('values'))
        extra_ok_ = True
        if key_ == 'sonico':
            b0_ = core.get('beta')
            extra_ok_ = bool(rec_.get('beta_ok') is True and rec_.get('alpha_two_names_same') is True and isinstance(vals_.get('beta'), float) and isinstance(b0_, float) and abs(vals_['beta'] - b0_) <= 1e-9 * abs(b0_)
                             and all(v_ is True for v_ in (rec_.get('cited_outside') or {}).values()) and bool(rec_.get('cited_outside')))
        V['pedras_kernel'][key_] = {'rel': rel_, 'flag': fl_, 'flag_true': flag_true_, 'theorem': th_, 'axioms': axr_.get(th_), 'source': src_.get(th_), 'contrato_ok': contrato_ok_, 'suporte_ok': suporte_ok_, 'n_contrato': len(contrato_), 'n_suporte': len(suporte_)}
        V[key_] = {'verdict': rec_.get('verdict'), 'ok': rec_.get('all_verified'), 'n_checks': mec_.get('n_checks'), 'checks_ok': checks_ok_, 'values': vals_, 'values_ok': values_ok_, 'beta_ok': rec_.get('beta_ok'), 'flag': fl_, 'flag_true': flag_true_, 'theorem': th_,
                   'in_trio': em_trio_(th_) if th_ else False, 'declared_in': src_.get(th_) if th_ else None}
        if not kernel_ok_:
            P.append('a pedra %s nao esta no kernel do rito como o ensaio a seco a pinou (bandeira True, composicao incondicional no trio, proveniencia no modulo da pedra, contrato e suporte no trio e no modulo certo, escada exata, fonte embutida)' % NOME_PEDRA_[key_])
        if not (rec_.get('all_verified') is True and rec_.get('does_not_gate_core') is True and rec_.get('runtime_executed') is True and checks_ok_ and values_ok_ and rec_.get('verdict') == ek_.get('verdict') and extra_ok_ and not rec_.get('guarda_p18_violacoes')):
            P.append('%s nao selou inteiro (selo, checagens numericas, numeros == ESPERADOS[%s], veredito do ensaio a seco, beta/inscricoes): ver o registro no core' % (rn_, key_))
        if key_ == 'afinacao':
            hy_ = rec_.get('hypothesis') or {}
            if not (hy_ == (ek_.get('hypothesis') or {'x': 1}) and hy_.get('status') == 'KNOWN' and hy_.get('named_not_proved') is True and rec_.get('geometry') == 'OPEN' and rec_.get('derives_strings_from_the_axiom') is False and vals_.get('kappa_from_core') is None
                    and list((rec_.get('auxiliaries_outside_the_composition') or {})) == list(ek_.get('auxiliares_fora_da_composicao') or ['x']) and all(v_ is True for v_ in (rec_.get('auxiliaries_outside_the_composition') or {}).values())):
                P.append('afinacao_das_cordas_v398: a hipotese MasslessFirstLevel deixou de ser KNOWN (nomeada, nao provada), ou a geometria deixou de ser OPEN, ou o kappa veio do core, ou a TGL passou a derivar cordas do axioma, ou os auxiliares fora da composicao mudaram')
    # cunhagens_v398: as SEIS inscricoes por sha256 (embedded_ok) e a sexta, e so' ela, ROTULADA como da gerencia (nunca fala do operador)
    cu = core.get('cunhagens_v398') or {}; kh = core.get('kh_n1_cobertura_v398') or {}
    cx_ = cu.get('extras') or {}; vb_ = cu.get('verbatim') or {}; ec_ = ESP.get('cunhagens') or {}
    ger_ = [k_ for k_, v_ in ec_.items() if str(v_.get('papel', '')).startswith('leitura da gerencia')]
    ger16_ = ger_[0][len('v398_cun_'):] if len(ger_) == 1 else None
    aut_ = cx_.get('autor_de_cada_inscricao') or {}
    rot_ok_ = bool(ger16_ and len(ec_) == 6 and aut_.get(ger16_) == 'gerencia' and sum(1 for a_ in aut_.values() if a_ == 'gerencia') == 1 and sum(1 for a_ in aut_.values() if a_ == 'operador') == len(ec_) - 1
                   and str((cx_.get('leitura_da_gerencia') or {}).get('sha16')) == ger16_ and str((cx_.get('leitura_da_gerencia') or {}).get('autor', '')).startswith('gerencia c1 (NAO e')
                   and aut_.get(str((cx_.get('leitura_da_gerencia') or {}).get('ratificada_pela_fala_de_sha16'))) == 'operador')
    verb_ok_ = bool(ec_) and set(vb_) == set(ec_) and all((vb_[k_] or {}).get('sha256') == ec_[k_]['sha256'] and (vb_[k_] or {}).get('embedded_ok') is True for k_ in ec_)
    pares_ok_ = all(isinstance(x_, list) and len(x_) == 2 and x_[0] == x_[1] for x_ in (cu.get('kernel') or {}).values()) and bool(cu.get('kernel'))
    V['cunhagens'] = {'n': len(vb_), 'verbatim_ok': verb_ok_, 'gerencia_sha16': ger16_, 'ratificada_pela': (cx_.get('leitura_da_gerencia') or {}).get('ratificada_pela_fala_de_sha16'), 'autores': aut_, 'rotulo_ok': rot_ok_, 'checks_ok': bool(cu.get('checks')) and all(c_.get('ok') is True for c_ in cu.get('checks')),
                      'n_checks': len(cu.get('checks') or []), 'verdict': cu.get('verdict'), 'kernel_ok': pares_ok_}
    if not (verb_ok_ and V['cunhagens']['checks_ok'] and pares_ok_ and cu.get('all_verified') is True and cu.get('does_not_gate_core') is True and cx_.get('teoremas') == ESP.get('teoremas_das_pedras') and cx_.get('bandeiras') == ESP.get('bandeiras_das_pedras')
            and cx_.get('n_bandeiras_por_pedra') == ESP.get('n_bandeiras_por_grupo') and cx_.get('n_bandeiras') == ESP.get('n_bandeiras_novas') and cx_.get('cunhagens_embutidas') == len(ec_) and cx_.get('auxiliares_da_afinacao_fora_da_composicao') == (ESP.get('afinacao') or {}).get('auxiliares_fora_da_composicao')):
        P.append('cunhagens_v398: as inscricoes embutidas nao sao as de ESPERADOS (sha256, embedded_ok), ou as checagens do registro, ou os teoremas/bandeiras das pedras diferem do ensaio a seco')
    if not rot_ok_:
        P.append('cunhagens_v398: a leitura da gerencia nao esta rotulada como da gerencia (autor_de_cada_inscricao: a sexta, e so\' ela, e\' da gerencia; as outras cinco, do operador; a ratificacao e\' de uma fala do operador)')
    cov = (core.get('kernel_formalization') or {}).get('axiom_coverage_v392') or {}   # o nome 'axiom_coverage_v392' e' do core (historico); segue na v398
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
