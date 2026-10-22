# -*- coding: utf-8 -*-
# LEITURA da rodada v386 -- SO LEITURA (nao executa codigo do um.py, do pacote nem do trabalhador). Todo numero, hash e veredito sai daqui, LIDO do
# artefato (o core, o selo, o stdout, o registro do pilar no core, o arquivo do pilar no Nos e a pasta (o cache) que o registro nomeia, o V1 do ramo B na
# pasta permanente da Bancada, o conferidor, o pacote v386, os backups de BYTES da v385 selada, os quatro arquivos do operador por sha256), nunca digitado.
# Molde: leitura_v385.py. Usado por superficies_v386, manifesto_v386, patch_arvore_indice_v386, handoff_v386, registrar_resultado_v386, compactar_memory_para_v386.
# PROBLEMAS (lista P) param a cadeia: o rito nao limpo, o conferidor reprovado (fora do aceite nomeado), o gate mudou, a escada != ESPERADOS, um veredito da
# v385 mudou, um modulo da v385 mudou de all_verified (comparado ao estado SELADO da v385 pelos backups de bytes), palavra proibida, um hash que nao bate, e
# todo registro v386 que nao selou (o Verbo, o ramo B por hash, a errata de R6, o reuse do pilar). O que o pilar DEU nao e' problema: reaproveitado (o
# esperado: sha256 e veredito = os da v385 selada) ou calculado de novo (dito, com a reprodutibilidade medida); so «nem um nem outro» e' problema.
# v386 (05/10/2026): le (a) O VERBO -- the_verb_v386 no core e no selo, as 110 declaracoes (93 da pedra + 17 da fiacao angular) no trio, a pedra no kernel do
# Nos por sha256 (e TGLExt.lean / TGL/Audit.lean trocados), o token lido do kernel; (b) O RAMO B -- ramo_b_preregistration_v386, o V1 em disco por sha256,
# o beta a 1e-9 relativo, os pinos, as erratas ao lado; (c) A ERRATA DE R6 -- ledger_errata_v386, o livro v383 intacto; (d) O PILAR -- quantum_pillar_reuse_v386
# (reaproveitado pela chave da v385, ou calculado de novo, dito) e a reprodutibilidade v385 sob reuse (NOT_COMPARED, esperado); (e) W10 -- a GPU na
# apresentacao, no resumo, nas palavras-chave e no sumario PT/EN; (f) AS PALAVRAS DO OPERADOR -- os quatro arquivos por sha256 (CANDIDATO_v386.json) e as
# decisoes de custodia/espelho/W10 do transcrito, cruzadas com o manifesto v385 arquivado (por hash) e com a memoria do Verbo; (g) a custodia v383/v384/v385 no git.
import os, re, json, glob, hashlib, time, datetime
import ambiente_v386 as A

HERE = os.path.dirname(os.path.abspath(__file__))
PK = A.PK; DAT = A.DAT
NOS_REAL = A.NOS_REAL
FINAL_RE = re.compile(r'^\[selo\] colapso tipado: ')
TRAILER_RE = re.compile(r'^(exit=\d+|rc=\d+|RITO_RC=\S+|inicio |fim )')
GUARDA = re.compile('(?<!NOT_)(?<!UN)' + 'CONF' + 'IRMED|(?<!AP)PRO' + 'VED_BY')
TRIO = {'propext', 'Classical.choice', 'Quot.sound'}
# os itens do conferidor congelado que falam SO do pilar (o resto -- gate, escada, vereditos, selo, artigo, md, Verbo, ramo B, errata -- nunca e' aceito como falha)
PILAR_ITENS = ("o pilar foi REAPROVEITADO pela chave da v385", "o registro do reuse v386 SELOU", "o resultado do pilar esta no Nos e no hash do selo",
               "o selo registra o mesmo veredito e o mesmo sha256 do resultado do pilar", "details.jsonl e cpuref.json da pasta do pilar",
               "o terceiro balde da custodia de sentido existe e esta vazio", "quantum_pillar_reproducibility_v385:",
               "o selo registra a reprodutibilidade igual ao core", "quantum_pillar_v384.reuse:")
REPRO_TXT = {'BIT_A_BIT': 'iguais bit a bit', 'ARREDONDAMENTO': 'iguais a menos de arredondamento', 'DIFERENTE': 'DIFERENTES (é resultado, e fica dito)',
             'NAO_COMPARADO': 'não comparados nesta rodada (o pilar não foi calculado: reaproveitado pela chave)', 'SEM_ANTERIOR': 'sem rodada anterior para comparar',
             'DESCONHECIDO': 'veredito da reprodutibilidade fora da forma do runtime'}
# AS PALAVRAS DO OPERADOR que os textos citam. Dois grupos:
# (1) dos QUATRO ARQUIVOS por sha256 (nome, chave do arquivo no CANDIDATO, ancora do inicio, ancora do fim (inclusive; None = ate o fim da linha), corte
#     antes?, corte depois?, [sic] fora das «»). O texto e' o trecho EXATO do arquivo; o corte e' marcado com «…» ao render.
VERBATINS_ARQ = (
    ('verbo_def', 'verbo_20261005_1653', 'Verbo=seleção da ação', None, False, False, None),
    ('verbo_tres', 'verbo_20261005_1653', 'O Verbo seleciona: nome, tempo e verdade', None, False, False, None),
    ('verbo_op', 'verbo_20261005_1653', 'O verbo é o operador de seleção da ação.', 'o objeto que será lido.', False, False, None),
    ('comando', 'verbo_20261005_1653', 'comando (que é a sujeição do verbo', 'conjugado, pareado)', True, True, 'cojuntamente'),
    ('circuito', 'verbo_20261005_1653', 'O verbo é a dobradiça entre o vazio e o objeto.', 'Sem leitura, não há axioma.', True, False, None),
    ('tres_eixos', 'verbo_20261005_1653', 'O verbo não seleciona uma coisa só.', 'a própria estrutura da realidade.', False, False, None),
    ('nome_fossil', 'verbo_20261005_1653', 'O nome é o ponto fixo do verbo.', 'o resultado é o nome:', False, True, None),
    ('comutacao', 'verbo_20261005_1653', 'Selecionar o nome defasa o tempo (a identidade resiste à mudança).', None, True, False, None),
    ('alpha2', 'verbo_20261005_1653', '[\\mathcal{V}_{\\text{nome}}, \\mathcal{V}_{\\text{tempo}}] = i\\alpha^2 \\, \\mathcal{V}_{\\text{erdade}}', None, False, False, None),
    ('constante', 'verbo_20261005_1653', 'A Constante de Miguel  é a constante de estrutura.', 'defasa os outros.', True, False, None),
    ('ramo_b', 'ramo_b_decision_20261005_1711', 'eu não havia proibido o ramo B', 'para prosseguir.', False, True, 'críterios'),
    ('ramo_b_pergunta', 'ramo_b_decision_20261005_1711', 'examinar se a constante de acoplamento', 'a constante da luz ao cubo', True, True, None),
    ('ramo_b_c3', 'ramo_b_decision_20261005_1711', 'desde antes sustentei que o regime gravitônico', 'correspondência direta com a proposta.', True, False, 'da fluxo'),
    ('ramo_b_resto', 'ramo_b_decision_20261005_1711', 'de resto concordo com tudo', None, True, False, None),
    ('luz_gravidade', 'respostas_20261005_1829', 'a luz como setor escuro', 'mas eles são indissociáveis', False, True, 'psionico'),
    ('leitor', 'respostas_20261005_1829', 'o leitor é indissociável da razão do objeto lido', 'for a existência.', True, False, None),
    ('verdade_custo', 'respostas_20261005_1829', 'são as duas faces do mesmo o objeto', 'jussivo à verdade', True, True, 'do mesmo o objeto'),
    ('anular', 'respostas_20261005_1829', 'reconhecer a identidade de determinado espectro', 'contorno geométrico da forma.', True, False, None),
    ('inscricao_custo', 'respostas_20261005_1829', 'é justamente a razão da inscrição que cria o custo', 'inexorável da existência.', True, False, 'condiçao'),
    ('tempo', 'respostas_20261005_1829', 'o tempo como fluxo da relatividade modular não pode ser dual', 'interdepend6encia relacional', True, True, 'interdepend6encia'),
    ('c3', 'respostas_20261005_1829', 'justamente por isso a constante da luz ao cubo', 'que seria a segunda leitura.', True, False, None),
    ('lagrangiana', 'respostas_20261005_1829', 'concordo plenamente quanto à lagrangiana', 'lagrangiana', False, True, None),
    ('nome_posto', 'respostas_20261005_1829', 'o Nome não é ontologia', 'com objeto distinto definido.', True, False, None),
    ('triade_posto', 'respostas_20261005_1829', 'todo "nome" atribuído a um objeto', 'posto absoluto', True, False, None),
    ('delegacao', 'respostas_20261005_1829', 'o resto vc consegue responder tudo agroa', None, False, False, 'agroa'),
)
# (2) do TRANSCRITO (mensagem achada pelo comeco; trecho por ancoras), CRUZADAS por hash: as de custodia/espelho com o manifesto v385 arquivado
#     (sha256 lido do MANIFESTO_ARQUIVO_v385.json), a ordem W10 com a memoria do Verbo (onde a errata de 05/10 a gravou entre «»).
VERBATINS_TR = (('custodia', 'excelente, conseguimos o que queríamos', 'antes de custodiar', 'tudo junto.', 'manifesto385'),
                ('espelho', 'excelente, conseguimos o que queríamos', 'penso que podemos espelhar', 'indexar a referência', 'manifesto385'),
                ('subpasta', 'Concordo como nome sugerido para a subpasta', 'Concordo como nome sugerido', 'para a subpasta', 'manifesto385'),
                ('v1_espelho', 'Concordo como nome sugerido para a subpasta', 'os V1-V1.3', 'vão ao espelho', 'manifesto385'),
                ('w10', 'verifique se a apresentação do artigo', 'verifique se a apresentação', None, 'memoria_verbo'))


def _textos_transcrito(d):
    if d.get('type') == 'user':
        c = d.get('message', {}).get('content'); return [c] if isinstance(c, str) else [x.get('text', '') for x in (c or []) if isinstance(x, dict) and x.get('type') == 'text']
    if d.get('type') == 'attachment' and (d.get('attachment') or {}).get('type') == 'queued_command':
        pr = d['attachment'].get('prompt'); return [pr] if isinstance(pr, str) else [x.get('text', '') for x in (pr or []) if isinstance(x, dict) and x.get('type') == 'text']
    return []


def palavras_do_transcrito(tr):
    """{nome: {'quando', 'quando_txt', 'texto'}} lido do transcrito; e a lista do que NAO foi achado."""
    msgs = []
    for line in open(tr, encoding='utf-8', errors='replace'):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if d.get('isCompactSummary') or d.get('isMeta'):
            continue
        for t in _textos_transcrito(d):
            t = (t or '').strip()
            if t and not t.startswith('<'):
                msgs.append((d.get('timestamp') or '', t))
    out, falta = {}, []
    for nome, comeco, a0, a1, _cruza in VERBATINS_TR:
        ms = [(ts, t) for ts, t in msgs if t.startswith(comeco)]
        if not ms:
            falta.append('%s: nenhuma mensagem do operador comeca com %r' % (nome, comeco)); continue
        ts, t = ms[-1]
        if len({x[1] for x in ms}) > 1:
            falta.append('%s: mais de uma mensagem DIFERENTE comeca com %r' % (nome, comeco)); continue
        i = t.find(a0)
        j = (t.find(a1, i) + len(a1)) if a1 is not None else len(t)
        if i < 0 or (a1 is not None and t.find(a1, i) < 0):
            falta.append('%s: a ancora nao esta na mensagem (%r / %r)' % (nome, a0, a1)); continue
        out[nome] = {'quando': ts, 'quando_txt': _hora_local(ts), 'texto': t[i:j], 'fonte': 'transcrito', 'pre': False, 'post': False, 'sic': None}
    return out, falta


def palavras_dos_arquivos(CM):
    """Os trechos dos QUATRO arquivos do operador, cada arquivo conferido por sha256 contra o CANDIDATO_v386.json (ordem_do_operador); e o que faltou."""
    out, falta, arqs = {}, [], {}
    ordem = CM.get('ordem_do_operador') or {}
    for k, p in A.OP_FILES.items():
        o = ordem.get(k) or {}
        try:
            b = open(p, 'rb').read()
        except OSError as e:
            falta.append('arquivo do operador %s nao lido: %r' % (k, e)); continue
        h = hashlib.sha256(b).hexdigest()
        ok = (h == o.get('sha256') and len(b) == int(o.get('bytes') or -1))
        arqs[k] = {'path': p, 'sha256': h, 'bytes': len(b), 'ok': ok, 'quando_utc': o.get('quando_utc')}
        if not ok:
            falta.append('arquivo do operador %s: sha256/bytes no disco (%s, %d) != CANDIDATO (%s, %s)' % (k, h[:16], len(b), str(o.get('sha256'))[:16], o.get('bytes')))
        t = b.decode('utf-8', errors='replace')
        if p.endswith('.json'):
            try:
                t = json.loads(t).get('verbatim') or ''
            except ValueError:
                t = ''
        arqs[k]['texto'] = t
    for nome, k, a0, a1, pre, post, sic in VERBATINS_ARQ:
        t = (arqs.get(k) or {}).get('texto') or ''
        i = t.find(a0)
        if i < 0:
            falta.append('%s: a ancora %r nao esta em %s' % (nome, a0[:40], k)); continue
        if a1 is None:
            j = t.find('\n', i); j = len(t) if j < 0 else j
        else:
            j = t.find(a1, i)
            if j < 0:
                falta.append('%s: a ancora de fim %r nao esta em %s' % (nome, a1[:40], k)); continue
            j += len(a1)
        if sic and sic not in t[i:j]:
            falta.append('%s: o [sic] %r nao esta no trecho' % (nome, sic))
        q = (arqs.get(k) or {}).get('quando_utc')
        out[nome] = {'quando': q, 'quando_txt': _hora_local(q), 'texto': t[i:j].rstrip('\r'), 'fonte': k, 'sha256': (arqs.get(k) or {}).get('sha256'), 'pre': pre, 'post': post, 'sic': sic}
    return out, falta, arqs


def render_op(o):
    """«…texto…» [sic: x] (hora) -- o corte marcado com «…», o [sic] FORA das «»."""
    if not o:
        return '«AUSENTE»'
    return '«%s%s%s»%s (%s)' % ('…' if o.get('pre') else '', o.get('texto', 'AUSENTE'), '…' if o.get('post') else '', (' [sic: %s]' % o['sic']) if o.get('sic') else '', o.get('quando_txt', 'n/d'))


def classe_da_reprodutibilidade(v):
    if '__REPRODUCED_BIT_FOR_BIT__' in v:
        return 'BIT_A_BIT'
    if '__REPRODUCED_WITHIN_ROUNDOFF__' in v:
        return 'ARREDONDAMENTO'
    if '__NOT_REPRODUCED__' in v:
        return 'DIFERENTE'
    if any(t_ in v for t_ in ('__NOT_COMPARED_THIS_RUN_DID_NOT_COMPUTE_A_RESULT__', '__NOT_COMPARED_DIFFERENT_INPUTS__', '__NOT_COMPARED_RUNTIME_ERROR__')):
        return 'NAO_COMPARADO'
    if '__NO_PREVIOUS_RUN_TO_COMPARE__' in v:
        return 'SEM_ANTERIOR'
    return 'DESCONHECIDO'


def classe_do_veredito(v, prefixo):
    if not v.startswith(prefixo):
        return 'DESCONHECIDO'
    if '__PARTIAL_RESULT_' in v:
        return 'PARCIAL'
    if '__CUSTODY_CHAIN_INCOMPLETE__' in v:
        return 'CUSTODIA_INCOMPLETA'
    if '__NOT_RUN__' in v:
        return 'NAO_RODOU'
    if '__RESULTS_VOID__' in v:
        return 'ANULADO'
    if '__ENGINE_SELFTEST_FAILED__' in v:
        return 'MOTOR_FALHOU'
    if re.search(r'__PHASE_T\d_FAILED__', v):
        return 'FASE_FALHOU'
    if v.startswith(prefixo + 'FIVE_JUMP_GKLS__'):
        return 'RAMO_9'
    return 'DESCONHECIDO'


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def _aplicado():
    ps = sorted(glob.glob(os.path.join(PK, 'APLICADO_AO_CANONICO_*.json')))
    assert ps, 'APLICADO_AO_CANONICO_*.json ausente no pacote v386'
    return json.load(open(ps[-1], encoding='utf-8')), ps[-1]


def _e(x, nd=2):
    return ('%.*e' % (nd, x)) if isinstance(x, (int, float)) and not isinstance(x, bool) and x == x else 'n/d'


def _num(x):
    return ('%g' % x).replace('.', ',') if isinstance(x, (int, float)) and not isinstance(x, bool) else 'n/d'


def _sim(x):
    return 'sim' if x is True else ('não' if x is False else 'não conferido nesta rodada')


def _hora_local(iso):
    try:
        d = datetime.datetime.strptime(str(iso)[:19], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=datetime.timezone.utc)
        l = d.astimezone(); off = l.strftime('%z')
        return '%s, hora local UTC%s%s:%s = %s UTC' % (l.strftime('%d/%m/%Y %H:%M:%S'), '−' if off[0] == '-' else '+', off[1:3], off[3:5], d.strftime('%H:%M:%S'))
    except (ValueError, TypeError, IndexError):
        return str(iso)


def _linhas_artigo(t):
    """as linhas do artigo .txt; no ensaio o marcador [SINTETICO] vai no FIM do arquivo (a linha 2 fica intacta)."""
    return [l for l in t.splitlines() if not l.startswith('[SINTETICO]')]


def ler():
    P = []
    amb = A.ambiente()
    nos = amb['nos']
    ESP = json.load(open(os.path.join(PK, 'ESPERADOS_v386.json'), encoding='utf-8'))
    CM = json.load(open(os.path.join(PK, 'CANDIDATO_v386.json'), encoding='utf-8'))
    ap, app = _aplicado()
    V = {'nos': nos, 'aplicado_json': app, 'sint_bool': amb['sint'], 'sint': ' [SINTÉTICO — ENSAIO DA CADEIA, NÃO É O RITO]' if amb['sint'] else ''}
    res = json.load(open(os.path.join(nos, 'um_absoluto.json'), encoding='utf-8'))
    selo = json.load(open(os.path.join(nos, 'um_absoluto_selo.json'), encoding='utf-8'))
    if amb['sint'] != bool(selo.get('SINTETICO_ENSAIO_V386')):
        P.append('a marca SINTETICO do Nos (%s) e a do selo (%s) divergem' % (amb['sint'], bool(selo.get('SINTETICO_ENSAIO_V386'))))
    stp = os.path.join(nos, 'rodada_v386_stdout.txt')
    out = open(stp, encoding='utf-8', errors='replace').read() if os.path.exists(stp) else ''
    if not out:
        P.append('rodada_v386_stdout.txt ausente ou vazio: o rito v386 nao rodou (ou nao acabou)')
    core = res['core']
    # ---- o um.py e a instalacao
    V['s64'] = sha(os.path.join(nos, 'um.py')); V['s16'] = V['s64'][:16]; V['umb'] = os.path.getsize(os.path.join(nos, 'um.py'))
    if str((selo.get('sha256') or {}).get('um.py', '')) != V['s64']:
        P.append('selo.sha256(um.py) != disco')
    if not (ap['um_py_novo']['sha16'] == V['s16'] == ESP['candidato_sha16'] == CM['sha16']):
        P.append('um.py do disco (%s) != o instalado (%s) / o candidato de ESPERADOS (%s) / CANDIDATO (%s)' % (V['s16'], ap['um_py_novo']['sha16'], ESP['candidato_sha16'], CM['sha16']))
    V['base16'] = ap['backups']['um.py']['sha16']
    if not (V['base16'] == ESP['origem_sha16'] == CM['base_v385_sha16']):
        P.append('a base substituida (%s) != a v385 selada de ESPERADOS/CANDIDATO (%s/%s)' % (V['base16'], ESP['origem_sha16'], CM['base_v385_sha16']))
    V['n_patches'] = len(CM.get('patches') or []); V['patches'] = ', '.join(p['id'] for p in CM.get('patches') or [])
    V['n_patches_w10'] = sum(1 for p in CM.get('patches') or [] if p['id'].startswith('W10'))
    if [p['id'] for p in CM.get('patches') or []] != ESP['patches']:
        P.append('os patches do CANDIDATO != os de ESPERADOS')
    V['kernel_decl'] = json.dumps(CM.get('kernel') or 'AUSENTE', ensure_ascii=False)
    V['instalado_em'] = '%s-%s-%s %s:%s:%s' % (ap['ts'][0:4], ap['ts'][4:6], ap['ts'][6:8], ap['ts'][9:11], ap['ts'][11:13], ap['ts'][13:15])
    try:
        _ens_p = os.path.join(PK, 'ensaio_a_seco_v386.json'); _ens = json.load(open(_ens_p, encoding='utf-8'))
        V['ensaio_seco'] = str(_ens.get('veredito'))
        if sha(_ens_p)[:16] != ESP.get('ensaio_sha16') or _ens.get('sha16') != CM['sha16'] or V['ensaio_seco'] != 'TUDO PASSOU':
            P.append('o ensaio a seco do pacote nao e o de ESPERADOS/do candidato ou nao passou (%s)' % V['ensaio_seco'])
    except Exception as e_:
        V['ensaio_seco'] = 'n/d'; P.append('o ensaio a seco nao foi lido: %r' % e_)
    # as tres afericoes adversariais (CONSTRUIR_v386_resultado.json), so para o texto
    try:
        _cp = os.path.join(DAT, 'CONSTRUIR_v386_resultado.json'); _C = json.load(open(_cp, encoding='utf-8'))
        _af = _C.get('afericoes') or []
        _it = []
        for a_ in _af:
            if isinstance(a_, dict):
                _rs = str(a_.get('resumo') or '')
                _mn = re.search(r'LENTE ([A-ZÀ-Ú0-9 ]+?)(?=\s*[—,.(]|\s*$)', _rs)
                nm = a_.get('lente') or a_.get('nome') or (('lente ' + _mn.group(1).strip().lower()) if _mn else 'lente ?')
                _ac = [x_ for x_ in (a_.get('achados') or []) if isinstance(x_, dict)]
                _gr = {}
                for x_ in _ac:
                    g_ = str(x_.get('gravidade') or '?').split(' ')[0].strip('(;:,'); _gr[g_] = _gr.get(g_, 0) + 1
                _it.append('%s: %d achado(s)%s%s' % (nm, len(_ac), (' — ' + ', '.join('%s %d' % (g_, n_) for g_, n_ in sorted(_gr.items()))) if _gr else '',
                                                    '; nada bloqueia' if 'Nada BLOQUEIA' in _rs else ''))
            else:
                _it.append(str(a_)[:60])
        V['n_afer'] = len(_af); V['afer_txt'] = '; '.join(_it) or 'n/d'; V['construir16'] = sha(_cp)[:16]
    except Exception as e_:
        V['n_afer'] = 'n/d'; V['afer_txt'] = 'n/d (%r)' % e_; V['construir16'] = 'AUSENTE'
    # ---- o stdout do rito
    m = re.search(r'teoremas limpos:\s*(\d+)/(\d+)', out)
    V['teor'] = '%s/%s' % m.groups() if m else 'AUSENTE'
    if not m or m.group(1) != m.group(2):
        P.append('teoremas limpos ausente ou N != M')
    elif [int(m.group(1)), int(m.group(2))] != [ESP['escada_v386'][1]] * 2:
        P.append('a escada do stdout (%s) != a esperada da v386 (%s/%s)' % (V['teor'], ESP['escada_v386'][1], ESP['escada_v386'][1]))
    m = re.search(r'(\d+) escritos, (\d+) inalterados', out)
    V['kmat'] = 'tgl_kernel: %s escritos, %s inalterados' % m.groups() if m else 'AUSENTE'
    V['selftest'] = 'FAIL_CLOSED_SELFTEST_PASSED' if 'FAIL_CLOSED_SELFTEST_PASSED' in out else 'AUSENTE'
    if V['selftest'] == 'AUSENTE' or selo.get('fail_closed_selftest') != 'FAIL_CLOSED_SELFTEST_PASSED':
        P.append('selftest nao PASSED (stdout ou selo)')
    if '>>> TGL_KERNEL_FORMALIZATION_FAILED <<<' in out or '>>> TGL_KERNEL_STAGE1_VERIFIED' not in out:
        P.append('a verificacao principal do kernel nao leu VERIFIED (linha >>> ... <<<)')
    if 'SEAL_WITHHELD' in out:
        P.append('o stdout traz SEAL_WITHHELD')
    m = re.search(r'\[selo\] rite_checkpoints: chave (\S+) ; reaproveitados (\d+)', out)
    V['ckpt'] = ('chave %s, %s reaproveitados' % m.groups()) if m else 'AUSENTE'
    V['compl'] = 'COMPLETA' if (m and m.group(1) == 'desligada' and m.group(2) == '0') else 'INTERMEDIÁRIA'
    if V['compl'] != 'COMPLETA':
        P.append('rodada nao COMPLETA (%s)' % V['ckpt'])
    sujo = [l for l in out.splitlines() if 'Traceback' in l or l.startswith('[selo] AVISO')]
    if sujo:
        P.append('stdout com Traceback/AVISO: %s' % sujo[:3])
    linhas = [l for l in out.splitlines() if l.strip() and not TRAILER_RE.match(l.strip())]
    if not linhas or not FINAL_RE.match(linhas[-1]):
        P.append('a ultima linha do stdout nao e a linha final do rito')
    mrc = re.findall(r'^RITO_RC=(\S+)', out, flags=re.M)
    V['rc'] = os.environ.get('V386_RC') or (mrc[-1] if mrc else 'NAO_LIDO')
    V['rcsrc'] = 'dito pela gerência (V386_RC)' if os.environ.get('V386_RC') else ('linha RITO_RC= do stdout (escrita pelo lançador rito_v386.sh)' if mrc else 'ausente')
    if V['rc'] != '0':
        P.append('rc do rito nao lido como 0 (%s)' % V['rc'])
    if mrc and os.environ.get('V386_RC') and mrc[-1] != os.environ['V386_RC']:
        P.append('V386_RC (%s) != RITO_RC do stdout (%s)' % (os.environ['V386_RC'], mrc[-1]))
    V['pilar_linhas'] = [l.strip() for l in out.splitlines() if ('[v384]' in l or 'pilar quantico' in l) and 'em curso' not in l]
    V['v386_linhas'] = [l.strip() for l in out.splitlines() if '[v386]' in l]
    V['n_v386_linhas'] = len(V['v386_linhas'])
    if V['n_v386_linhas'] < 4:
        P.append('o stdout tem %d linha(s) [v386] (esperadas >= 4: o reuse, o Verbo, o ramo B, a errata)' % V['n_v386_linhas'])
    mb = re.search(r'\[selo\] custodia de sentido: .*\| computacao nao concluida: (.*)$', out, flags=re.M)
    V['balde_stdout'] = mb.group(1).strip() if mb else 'AUSENTE'
    if not mb:
        P.append('a linha da custodia de sentido nao nomeia o terceiro balde (W08c)')
    hor = amb['horarios']
    hh = open(hor, encoding='utf-8').read().split() if os.path.exists(hor) else []
    V['t0'] = hh[0] if hh else 'n/d'
    V['t1'] = hh[1] if len(hh) > 1 else (time.strftime('%H:%M:%S', time.localtime(os.stat(stp).st_mtime)) if os.path.exists(stp) else 'n/d')
    V['tsrc'] = 'horários gravados pelo lançador rito_v386.sh' if len(hh) > 1 else 'fim = última modificação do stdout (o lançador não gravou o horário de fim)'
    V['tentativas'] = sorted(os.path.basename(p) for p in glob.glob(os.path.join(nos, 'rodada_v386_stdout_tentativa*.txt')))
    V['selo_ts'] = str(selo.get('timestamp'))
    if not (V['selo_ts'] >= V['instalado_em']):
        P.append('o selo (%s) e anterior a instalacao da v386 (%s): o rito nao selou a v386' % (V['selo_ts'], V['instalado_em']))
    # ---- o conferidor (copia byte a byte do pacote, rodada em v386_selo\conferidor)
    cdir = amb['conf_dir']
    confp = os.path.join(cdir, 'conferencia_rito_v386.json'); confo = os.path.join(cdir, 'conferir_rito_v386_stdout.txt')
    try:
        C = json.load(open(confp, encoding='utf-8')); CO = open(confo, encoding='utf-8', errors='replace').read()
    except OSError as e:
        C, CO = {}, ''; P.append('conferidor nao lido: %r' % e)
    dm = C.get('deve_mudar') or {}; npm = C.get('nao_pode_mudar') or {}; mdd = C.get('muda_e_e_dito') or {}
    V['conf_dm'] = '%d/%d' % (sum(1 for v in dm.values() if v), len(dm)); V['conf_np'] = '%d/%d' % (sum(1 for v in npm.values() if v), len(npm))
    V['conf_md'] = '%d/%d' % (sum(1 for v in mdd.values() if v), len(mdd))
    V['conf16'] = sha(confp)[:16] if os.path.exists(confp) else 'AUSENTE'
    V['conf_falhas'] = [k for k, v in list(dm.items()) + list(npm.items()) + list(mdd.items()) if not v]
    V['servidor'] = str(C.get('servidor_depois_do_rito') or 'n/d'); V['avisos_lancador'] = len(C.get('avisos_do_lancador') or []); V['sinais'] = len(C.get('sinais_desta_rodada') or [])
    V['conf_aceite'] = ''
    if C.get('um_py_sha16') != V['s16']:
        P.append('o conferidor conferiu outro um.py (%s)' % C.get('um_py_sha16'))
    if not (C.get('tudo_bate') is True and CO.rstrip().endswith('TUDO BATE')):
        so_pilar = bool(V['conf_falhas']) and all(any(k.startswith(p) for p in PILAR_ITENS) for k in V['conf_falhas'])
        ac = os.environ.get('V386_ACEITO_PILAR_NAO_CONCLUIDO')
        if ac and ac == V['conf16'] and so_pilar:
            V['conf_aceite'] = ('o conferidor congelado reprovou SÓ itens do pilar (%d: %s); a gerência aceitou o resultado do pilar como resultado, '
                                'pela conferência `%s` nomeada (V386_ACEITO_PILAR_NAO_CONCLUIDO)' % (len(V['conf_falhas']), '; '.join(V['conf_falhas']), V['conf16']))
        else:
            P.append('conferidor NAO deu TUDO BATE para este um.py (falhas: %s%s)' % (V['conf_falhas'][:6], '; SO itens do pilar -- decisao da gerencia (V386_ACEITO_PILAR_NAO_CONCLUIDO=<sha16 da conferencia>)' if so_pilar else ''))
    # ---- o kernel e o gate (o MESMO da v385)
    kf = core.get('kernel_formalization') or {}
    V['n_flags_true'] = sum(1 for k, v in kf.items() if v is True)
    _ft = sorted(k for k, v in kf.items() if v is True)
    if _ft != sorted(set(ESP['flags_true_v385']) | set(ESP['flags_v386'])):
        P.append('as bandeiras True do kernel (%d) != as da v385 (%d) + as %d da v386' % (V['n_flags_true'], len(ESP['flags_true_v385']), len(ESP['flags_v386'])))
    if {k: kf.get(k) for k in ESP['flags_gpf_gpc_gpi_v385']} != ESP['flags_gpf_gpc_gpi_v385']:
        P.append('as bandeiras gpf_/gpc_/gpi_ mudaram')
    V['termo'] = {k: kf.get(k) for k in ('gpf_H2_smooth_modular_four_frame_discharged', 'gpf_H3_local_horizon_equilibrium_discharged', 'gpi_H3_horizon_data_produced')}
    V['hvals'] = '/'.join(str(v) for v in V['termo'].values())
    lad = core.get('external_ladder') or {}
    V['esc'] = '%s/%s' % (lad.get('n_theorems_clean'), lad.get('n_theorems_expected'))
    if [lad.get('n_theorems_clean'), lad.get('n_theorems_expected')] != [ESP['escada_v386'][1]] * 2:
        P.append('a escada do core (%s) != a esperada da v386 (%s/%s)' % (V['esc'], ESP['escada_v386'][1], ESP['escada_v386'][1]))
    V['esc_v385'] = '%s/%s' % tuple(ESP['escada_v385'])
    V['nax'] = len(kf.get('axiom_report') or {})
    if any('sorryAx' in a for v in (kf.get('axiom_report') or {}).values() for a in (v or [])):
        P.append('sorryAx no axiom_report')
    Vd = lambda k: str((core.get(k) or {}).get('verdict') or 'AUSENTE')
    dif = {k: (v, Vd(k)) for k, v in ESP['vereditos_v385'].items() if Vd(k) != v}
    V['n_ver'] = len(ESP['vereditos_v385']); V['n_ver_iguais'] = V['n_ver'] - len(dif)
    if dif:
        P.append('%d veredito(s) da v385 mudaram: %s' % (len(dif), list(dif)[:5]))
    V['livro'] = Vd('the_ledger_of_charges_v383'); V['iald'] = Vd('the_iald_index'); V['ax_v385'] = Vd('the_axiom_v385')
    if (core.get('the_iald_index') or {}).get('all_verified') is not True:
        P.append('the_iald_index nao selado (all_verified != True)')
    if (core.get('the_axiom_v385') or {}).get('all_verified') is not True:
        P.append('the_axiom_v385 nao selou de novo (all_verified != True)')
    V['qg'] = str(selo.get('qg_closure_verdict'))
    if V['qg'] != ESP['qg_closure_verdict_v385']:
        P.append('o gate MUDOU (%s)' % V['qg'])
    qg = core.get('qg_closure') or {}
    V['n18'] = sum(1 for fam in ('formal_flags', 'physics_flags', 'experiment_flags') for v in (qg.get(fam) or {}).values() if v is True)
    if V['n18'] != 18:
        P.append('as bandeiras do gate nao sao 18/18 (%d)' % V['n18'])
    fr = (qg.get('gate') or {}).get('kernel_frontier') or {}
    V['remaining'] = ', '.join(fr.get('remaining') or []) or 'n/d'
    V['after_cit'] = fr.get('remaining_after_citation_v374')
    if V['after_cit'] != []:
        P.append('remaining_after_citation_v374 nao e [] (%s)' % V['after_cit'])
    cf = core.get('tetelestai_conference_v376') or {}
    V['cf_counts'] = ', '.join('%s %s' % (k, v) for k, v in (cf.get('counts') or {}).items()); V['abertos'] = cf.get('open_items')
    if cf.get('consummated') is not True or V['abertos'] != []:
        P.append('a conferencia v376 (pinada) nao le consumada nesta rodada')
    V['fse'] = selo.get('full_static_witness_exists')
    if V['fse'] is not False:
        P.append('full_static_witness_exists nao e False')
    # ---- o selo da v386
    V['um_version'] = str(selo.get('um_version'))
    if V['um_version'] != 'v386':
        P.append('selo.um_version != v386 (%s): o rito ainda nao selou a v386' % V['um_version'])
    if not all(selo.get(k) == v for k, v in ESP['selo_leituras_pinadas'].items()):
        P.append('as leituras v377-v385 do selo mudaram')
    if selo.get('final_step_name_v385') != ESP['final_step_name_v385'] or selo.get('the_axiom_v385') != (ESP.get('selo_registros_v385_pinados') or {}).get('the_axiom_v385'):
        P.append('final_step_name_v385 / the_axiom_v385 do selo mudaram')
    V['vb_reading'] = str(selo.get('the_verb_reading_v386') or 'AUSENTE')
    if V['vb_reading'] == 'AUSENTE' or GUARDA.search(V['vb_reading']) or 'TGL_PRO' + 'VED' in V['vb_reading']:
        P.append('a leitura the_verb_reading_v386 do selo ausente ou com palavra proibida')
    V['vb_token_selo'] = str(selo.get('verb_typing_stone_name_v386') or 'AUSENTE')
    if V['vb_token_selo'] != ESP['verb_token']:
        P.append('verb_typing_stone_name_v386 do selo (%s) != o token de ESPERADOS' % V['vb_token_selo'][:60])
    nst = selo.get('not_sealed_this_run') or {}
    V['formais'] = ', '.join(nst.get('formais') or []) or 'nenhum'
    if sorted(nst.get('formais') or []) != ESP['not_sealed_formais_v385']:
        P.append('os formais nao selados mudaram (%s)' % nst.get('formais'))
    if 'computacao_nao_concluida' not in nst:
        P.append('o terceiro balde (computacao_nao_concluida) nao existe no selo')
    V['balde_l'] = list(nst.get('computacao_nao_concluida') or [])
    V['balde'] = ', '.join(V['balde_l']) or 'nenhuma'
    if V['balde_stdout'] not in ('AUSENTE', V['balde']):
        P.append('o terceiro balde do stdout (%s) != o do selo (%s)' % (V['balde_stdout'], V['balde']))
    V['recusas'] = ', '.join(sorted(nst.get('recusas_de_dado') or [])) or 'nenhuma'
    if sorted(nst.get('recusas_de_dado') or []) != sorted(ESP['not_sealed_recusas_v385']):
        P.append('o balde das recusas de dado mudou (%s)' % V['recusas'])
    # ---- o estado SELADO da v385, pelos backups de BYTES do Nos (conferidos pelo sha16 do APLICADO): all_verified de TODO modulo igual
    try:
        _bk = ap['backups']
        _cb = open(_bk['um_absoluto.json']['backup'], 'rb').read(); _sb = open(_bk['um_absoluto_selo.json']['backup'], 'rb').read()
        if hashlib.sha256(_cb).hexdigest()[:16] != _bk['um_absoluto.json']['sha16'] or hashlib.sha256(_sb).hexdigest()[:16] != _bk['um_absoluto_selo.json']['sha16']:
            raise ValueError('os backups da v385 no Nos nao batem com o sha16 do APLICADO')
        C385 = json.loads(_cb.decode('utf-8'))['core']; S385 = json.loads(_sb.decode('utf-8'))
        if S385.get('um_version') != 'v385':
            raise ValueError('o backup do selo nao e da v385 (%s)' % S385.get('um_version'))
        av385 = {k: m_.get('all_verified') for k, m_ in C385.items() if isinstance(m_, dict) and 'all_verified' in m_}
        difav = sorted(k for k, v in av385.items() if (core.get(k) or {}).get('all_verified') != v)
        V['n_av'] = len(av385); V['n_av_iguais'] = len(av385) - len(difav)
        if difav:
            P.append('%d modulo(s) da v385 mudaram de all_verified em relacao ao estado SELADO: %s' % (len(difav), difav[:6]))
        V['selo385_ts'] = str(S385.get('timestamp'))
    except Exception as e_:
        V['n_av'] = V['n_av_iguais'] = 'n/d'; V['selo385_ts'] = 'n/d'
        P.append('o estado selado da v385 (backups de bytes no Nos) nao foi lido: %r' % e_)
    _mds = [os.path.join(nos, 'um_absoluto_forma_canonica.md'), os.path.join(nos, 'um_absoluto_manifest.md')]
    _mtx = [open(p, encoding='utf-8', errors='replace').read() if os.path.exists(p) else '' for p in _mds]
    _car = all(ESP['md_carimbo'] in t and ('sha256/16 `%s`' % V['s16']) in t for t in _mtx)
    V['md_carimbo'] = 'SIM (forma canônica + manifesto)' if _car else 'NÃO'
    if not _car:
        P.append('os .md emitidos nao trazem o carimbo v386 com o sha16 do um.py do disco')
    _fc = _mtx[0]
    V['md_errata_R6'] = _sim(ESP['md_errata_R6'] in _fc); V['md_errata_posto_fica'] = _sim(ESP['md_errata_posto_v385_fica'] in _fc)
    V['md_registros_v386'] = '%d de 4' % sum(1 for k in ('the_verb_v386', 'ramo_b_preregistration_v386', 'ledger_errata_v386', 'quantum_pillar_reuse_v386') if k in _fc)
    if not (ESP['md_errata_R6'] in _fc and ESP['md_errata_posto_v385_fica'] in _fc and V['md_registros_v386'] == '4 de 4'):
        P.append('o .md canonico nao traz a errata de R6 / a errata do posto que fica / os 4 registros v386')
    # ---- (v386) A PEDRA e os dois .lean trocados, no kernel do Nos, por sha256
    _st = os.path.join(nos, 'tgl_kernel', 'TGLExt', 'TheVerbSelectsTheAction.lean')
    V['vb_pedra16'] = sha(_st)[:16] if os.path.exists(_st) else 'AUSENTE'
    if V['vb_pedra16'] != ESP['kernel']['new']['TGLExt/TheVerbSelectsTheAction.lean']:
        P.append('a pedra no kernel do Nos (%s) nao e a do candidato (%s)' % (V['vb_pedra16'], ESP['kernel']['new']['TGLExt/TheVerbSelectsTheAction.lean']))
    for rel, key in (('TGLExt.lean', 'stone_tglext16'), (os.path.join('TGL', 'Audit.lean'), 'stone_audit16')):
        p_ = os.path.join(nos, 'tgl_kernel', rel); V[key] = sha(p_)[:16] if os.path.exists(p_) else 'AUSENTE'
        esp_ = ESP['kernel']['changed'][rel.replace(os.sep, '/')][1]
        if V[key] != esp_:
            P.append('%s no kernel do Nos (%s) != o do candidato (%s)' % (rel, V[key], esp_))
    try:
        _pp = json.load(open(os.path.join(DAT, 'kernel', 'PEDRA_v386_pos_build.json'), encoding='utf-8'))
        V['vb_pedra_bytes'] = _pp.get('bytes'); V['vb_pedra_linhas'] = _pp.get('linhas'); V['vb_build'] = '%s → %s' % (_pp.get('build_inicio'), _pp.get('build_fim'))
        if str(_pp.get('sha256', ''))[:16] != V['vb_pedra16']:
            P.append('PEDRA_v386_pos_build.json (%s) != a pedra no kernel do Nos (%s)' % (str(_pp.get('sha256'))[:16], V['vb_pedra16']))
    except Exception as e_:
        V['vb_pedra_bytes'] = V['vb_pedra_linhas'] = 'n/d'; V['vb_build'] = 'n/d'; P.append('PEDRA_v386_pos_build.json nao lido: %r' % e_)
    _axr = kf.get('axiom_report') or {}
    _fora = [n for n in ESP['nomes_lean_v386'].values() if _axr.get(n) is None or not set(_axr.get(n) or []) <= TRIO]
    V['vb_decl'] = '%d de %d' % (len(ESP['nomes_lean_v386']) - len(_fora), len(ESP['nomes_lean_v386']))
    if _fora:
        P.append('declaracoes da v386 fora do trio ou ausentes do axiom_report: %s' % _fora[:4])
    V['vb_n_pedra'] = sum(1 for f in ESP['flags_v386'] if f.startswith('ext_vrb_')); V['vb_n_ang'] = sum(1 for f in ESP['flags_v386'] if f.startswith('ext_ang_'))
    V['vb_n_total'] = len(ESP['flags_v386'])
    # ---- (v386) O VERBO: o registro no core e no selo
    vb = core.get('the_verb_v386') or {}; svb = selo.get('the_verb_v386') or {}
    V['vb_v'] = str(vb.get('verdict') or 'AUSENTE')
    V['vb_ok'] = '%s de %s' % (vb.get('kernel_flags_ok'), vb.get('kernel_flags_total'))
    V['vb_vrb'] = '%s de %s' % (vb.get('vrb_ok'), vb.get('vrb_total')); V['vb_ang'] = '%s de %s' % (vb.get('ang_ok'), vb.get('ang_total'))
    V['vb_token'] = str(vb.get('token_from_kernel') or 'AUSENTE'); V['vb_token_ok'] = _sim(vb.get('token_matches_kernel')); V['vb_verbatim_ok'] = _sim(vb.get('verbatim_hashes_ok'))
    V['vb_delegation'] = str(vb.get('delegation') or 'AUSENTE')
    V['vb_files'] = {k: {'sha256': str((f or {}).get('sha256')), 'ok': (f or {}).get('embedded_matches_sha256'), 'on_disk': (f or {}).get('on_disk_matches'), 'quando_utc': (f or {}).get('quando_utc')}
                     for k, f in (vb.get('verbatim_files') or {}).items()}
    V['vb_files_txt'] = '; '.join('%s `%s` (%s)' % (k, f['sha256'][:16], 'confere' if f['ok'] else 'NÃO confere') for k, f in V['vb_files'].items()) or 'n/d'
    V['vb_not_typed'] = '; '.join(vb.get('what_is_not_typed') or []) or 'n/d'
    if not (vb.get('all_verified') is True and vb.get('kernel_flags_ok') == vb.get('kernel_flags_total') == len(ESP['flags_v386']) and vb.get('token_matches_kernel') is True
            and V['vb_token'] == ESP['verb_token'] and vb.get('verbatim_hashes_ok') is True and V['vb_v'].startswith('TGL_THE_VERB_V386__THE_VERB_SELECTS_THE_ACTION__')
            and V['vb_v'].endswith('__GATE_UNTOUCHED__PROVED_IS_NOT_CONFIRMED')):
        P.append('o Verbo nao selou nesta rodada (%s; token %s; verbatim %s; %s)' % (V['vb_ok'], V['vb_token_ok'], V['vb_verbatim_ok'], V['vb_v'][:90]))
    if svb.get('verdict') != vb.get('verdict') or any(svb.get(k_) != vb.get(k_) for k_ in ('all_verified', 'kernel_flags_ok', 'kernel_flags_total', 'token_from_kernel', 'verbatim_hashes_ok')):
        P.append('o registro do Verbo no selo != o do core')
    if GUARDA.search(V['vb_v']) or 'TGL_PRO' + 'VED' in V['vb_v']:
        P.append('o veredito do Verbo traz palavra proibida')
    # ---- (v386) O RAMO B: o registro, e o V1 em disco por sha256 (so leitura da pasta permanente da Bancada)
    rb = core.get('ramo_b_preregistration_v386') or {}; srb = selo.get('ramo_b_preregistration_v386') or {}
    V1 = ESP['ramo_b_V1']
    V['rb_v'] = str(rb.get('verdict') or 'AUSENTE'); V['rb_id'] = str(rb.get('identificador_read') or 'AUSENTE')
    _sr = rb.get('sha256_read') or {}
    V['rb_json64'] = str(_sr.get('json') or 'AUSENTE'); V['rb_md64'] = str(_sr.get('md') or 'AUSENTE'); V['rb_hashes64'] = str(_sr.get('hashes') or 'AUSENTE')
    V['rb_json16'] = V['rb_json64'][:16]; V['rb_md16'] = V['rb_md64'][:16]; V['rb_hashes16'] = V['rb_hashes64'][:16]
    V['rb_spec64'] = str(rb.get('spec_sha256_recomputed') or 'AUSENTE'); V['rb_spec16'] = V['rb_spec64'][:16]
    V['rb_nD'] = rb.get('conjunto_D_n'); V['rb_F2b'] = str(rb.get('F2b_status')); V['rb_qual'] = str(rb.get('F2b_qualifier')); V['rb_vered_v1'] = str(rb.get('veredito_do_V1'))
    V['rb_token_estado'] = str(rb.get('token_estado') or 'AUSENTE')
    _b = rb.get('beta') or {}
    V['rb_beta_v1'] = _b.get('v1'); V['rb_beta_core'] = _b.get('core'); V['rb_abs'] = _e(_b.get('abs_diff')); V['rb_rel'] = _e(_b.get('rel_diff')); V['rb_beta_ok'] = _sim(rb.get('beta_ok'))
    V['rb_beta_v1_txt'] = ('%.18g' % _b['v1']) if isinstance(_b.get('v1'), float) else 'n/d'; V['rb_beta_core_txt'] = ('%.18g' % _b['core']) if isinstance(_b.get('core'), float) else 'n/d'
    _pins = rb.get('pins') or {}
    V['rb_pins_n'] = len(_pins); V['rb_pins_ok'] = _sim(rb.get('pins_ok')); V['rb_pins_iguais'] = sum(1 for p_ in _pins.values() if (p_ or {}).get('equal'))
    V['rb_poder_A31'] = _num(((_pins.get('poder_exato_A31') or {}).get('read'))); V['rb_sigma_beta_lido_A31'] = _num(((_pins.get('sigma_beta_lido_A31') or {}).get('read')))
    V['rb_erratas_l'] = list(rb.get('erratas_ao_lado') or []); V['rb_erratas_n'] = len(V['rb_erratas_l'])
    V['rb_central_txt'] = str(rb.get('central_values_transcribed_from_sealed_registry_NOT_BLIND') or 'n/d')
    V['rb_files_ok'] = _sim(rb.get('files_ok')); V['rb_hashes_ok'] = _sim(rb.get('hashes_file_ok')); V['rb_recompute_ok'] = _sim(rb.get('recompute_ok'))
    V['rb_nothing_opened'] = _sim(rb.get('nothing_opened')); V['rb_v387'] = str(rb.get('v387') or '')
    if not (rb.get('all_verified') is True and rb.get('read_ok') is True and V['rb_nD'] == V1['conjunto_D_n'] == 14 and V['rb_json64'] == V1['files']['json']['sha256']
            and V['rb_id'] == V1['identificador'] and V['rb_spec64'] == V1['spec_sha256'] and V['rb_v'].startswith('TGL_RAMO_B_PREREGISTERED_V386__V1_READ_BY_HASH_' + V1['files']['json']['sha256'][:16])
            and V['rb_v'].endswith('__AWAITING_DATA__NOTHING_OPENED__GATE_UNTOUCHED') and rb.get('nothing_opened') is True and V['rb_F2b'] == 'AWAITING'
            and V['rb_vered_v1'] == V1['veredito_do_V1'] and V['rb_token_estado'] == V1['token_estado'] and rb.get('beta_ok') is True and rb.get('pins_ok') is True):
        P.append('o ramo B nao foi lido por hash nesta rodada como esperado (%s; read_ok %s; D %s; F2b %s)' % (V['rb_v'][:80], rb.get('read_ok'), V['rb_nD'], V['rb_F2b']))
    if srb.get('verdict') != rb.get('verdict') or any(srb.get(k_) != rb.get(k_) for k_ in ('all_verified', 'read_ok', 'sha256_read', 'spec_sha256_recomputed', 'conjunto_D_n', 'F2b_status', 'pins')):
        P.append('o registro do ramo B no selo != o do core')
    if rb.get('forbidden_words_in_transcribed_fields'):
        P.append('palavra proibida nos campos transcritos do V1: %s' % rb.get('forbidden_words_in_transcribed_fields'))
    if GUARDA.search(V['rb_v']) or 'TGL_PRO' + 'VED' in V['rb_v']:
        P.append('o veredito do ramo B traz palavra proibida')
    # o V1 em disco (a pasta permanente), por sha256 e bytes, contra os ESPERADOS; e o que o V1 diz (k, M, lugar, identificacao, ratificacao, delegacao)
    V['rb_disk'] = {}
    for k_, f_ in V1['files'].items():
        p_ = f_['path']
        ok_ = os.path.isfile(p_) and sha(p_) == f_['sha256'] and os.path.getsize(p_) == f_['bytes']
        V['rb_disk'][k_] = ok_
        if not ok_:
            P.append('o V1 do ramo B em disco (%s) nao e o pinado nos ESPERADOS' % k_)
    V['rb_disk_txt'] = '%d de %d arquivos do V1 em disco com o sha256 e os bytes pinados' % (sum(1 for x in V['rb_disk'].values() if x), len(V['rb_disk']))
    try:
        import stat as _st
        V['rb_so_leitura'] = _sim(all(not (os.stat(f_['path']).st_mode & _st.S_IWRITE) for f_ in V1['files'].values()))
    except OSError:
        V['rb_so_leitura'] = 'n/d'
    try:
        PJ = json.loads(open(V1['files']['json']['path'], 'rb').read().decode('utf-8'))
        sp = PJ.get('spec') or {}
        V['rb_k'] = str((sp.get('k') or {}).get('escolha')); V['rb_k_chi0'] = _num((sp.get('k') or {}).get('em_chi_0')); V['rb_M'] = str((sp.get('M_X') or {}).get('escolha'))
        V['rb_lugar'] = str((sp.get('tau_star') or {}).get('lugar')); V['rb_forma'] = str((sp.get('tau_star') or {}).get('forma'))
        V['rb_ident_prim'] = str((sp.get('identificacao') or {}).get('primaria')); V['rb_ident_sec'] = str((sp.get('identificacao') or {}).get('secundaria'))
        _D = (sp.get('conjuntos') or {}).get('D') or {}
        V['rb_D_sem_hold'] = _D.get('n_sem_pendencia_de_quality') or _D.get('n_sem_pendencia_de_qualidade'); V['rb_D_hold'] = len(_D.get('com_data_quality_hold') or [])
        V['rb_D_cand'] = _D.get('n_test_candidates')
        _vp = sp.get('vereditos_permitidos_na_ordem') or []
        V['rb_vereditos_ordem'] = ' → '.join(str(v_.get('token')) for v_ in _vp if isinstance(v_, dict)) or 'n/d'
        # a lista dos vereditos proibidos NAO se transcreve (ela contem as proprias palavras que a guarda do rito veda): so a contagem, e onde esta
        V['rb_vereditos_proibidos_l'] = [str(x) for x in (sp.get('vereditos_proibidos') or [])]
        V['rb_vereditos_proibidos'] = '%d tokens vedados pela régua (a mesma guarda do rito; a lista está no V1, `spec.vereditos_proibidos`)' % len(V['rb_vereditos_proibidos_l'])
        _rt = PJ.get('ratificacao') or {}
        V['rb_ratif_tipo'] = str(_rt.get('tipo')); V['rb_ratif_quando'] = str(_rt.get('quando_utc')); V['rb_ratif_quando_txt'] = _hora_local(_rt.get('quando_utc'))
        V['rb_ratif_verbatim'] = str(_rt.get('verbatim')); V['rb_ratif_sha_txt'] = str(_rt.get('verbatim_inteiro_sha256_txt'))
        V['rb_ratif_sha_json_registrado'] = str(_rt.get('sha256_json'))
        _dd = PJ.get('decisoes_por_delegacao') or []
        V['rb_decisoes_ns'] = ', '.join(str(d_.get('n')) for d_ in _dd if isinstance(d_, dict)) or 'n/d'; V['rb_n_decisoes'] = len(_dd)
        V['rb_gerado_utc'] = str(PJ.get('gerado_utc'))
        if V['rb_ratif_verbatim'] != 'o resto vc consegue responder tudo agroa' or V['rb_ratif_sha_txt'] != (CM.get('ordem_do_operador') or {}).get('respostas_20261005_1829', {}).get('sha256'):
            P.append('a ratificacao do V1 do ramo B nao e a delegacao do operador por hash (%s / %s)' % (V['rb_ratif_verbatim'][:40], V['rb_ratif_sha_txt'][:16]))
    except Exception as e_:
        for k_ in ('rb_k', 'rb_k_chi0', 'rb_M', 'rb_lugar', 'rb_forma', 'rb_ident_prim', 'rb_ident_sec', 'rb_D_sem_hold', 'rb_D_hold', 'rb_D_cand', 'rb_vereditos_ordem', 'rb_vereditos_proibidos',
                   'rb_ratif_tipo', 'rb_ratif_quando', 'rb_ratif_quando_txt', 'rb_ratif_verbatim', 'rb_ratif_sha_txt', 'rb_ratif_sha_json_registrado', 'rb_decisoes_ns', 'rb_gerado_utc'):
            V[k_] = 'n/d'
        V['rb_n_decisoes'] = 'n/d'; P.append('o V1 do ramo B nao foi lido do disco: %r' % e_)
    # a errata do RESPOSTAS json («agroa»), lida do CANDIDATO (o V1 congelado registra o sha256 anterior)
    _re = CM.get('respostas_json_errata_ao_lado') or {}
    V['rb_errata_json_txt'] = ('o `RESPOSTAS_operador_05out.json` ganhou a errata [sic] («tudo agroa») DEPOIS do congelamento do V1: o V1 registra o sha256 anterior `%s`; o de hoje é `%s`; backup de bytes `%s`'
                               % (str(_re.get('sha256_registrado_no_V1_congelado'))[:16], str((CM.get('ordem_do_operador') or {}).get('respostas_json_20261005_1829', {}).get('sha256'))[:16], _re.get('backup_bytes_dessa_versao')))
    _ee = CM.get('espec_errata_ao_lado') or {}
    V['rb_espec_errata16'] = str(_ee.get('sha256') or 'AUSENTE')[:16]; V['rb_espec16'] = str(_ee.get('espec_original_sha256') or 'AUSENTE')[:16]
    try:
        _ep = os.path.join(DAT, 'ramo_b', 'ESPEC_RUNTIME_RAMO_B_v386_ERRATA.json'); _E2 = json.load(open(_ep, encoding='utf-8'))
        if sha(_ep) != _ee.get('sha256'):
            P.append('a errata da ESPEC em disco != o sha256 do CANDIDATO')
        V['rb_espec_erratas'] = ', '.join(sorted((_E2.get('erratas') or {}).keys())) or 'n/d'
    except Exception as e_:
        V['rb_espec_erratas'] = 'n/d'; P.append('a errata da ESPEC nao foi lida: %r' % e_)
    _bv = CM.get('beta_v1_vs_core') or {}
    V['cm_beta_rule'] = str(_bv.get('rule') or 'n/d')
    # ---- (v386) A ERRATA AO LADO DE R6
    le = core.get('ledger_errata_v386') or {}; sle = selo.get('ledger_errata_v386') or {}
    V['le_v'] = str(le.get('verdict') or 'AUSENTE'); V['le_n'] = le.get('v383_n_charges'); V['le_intacto'] = _sim(le.get('v383_ledger_intact'))
    _f2b = le.get('charge_F2b') or {}
    V['le_f2b_token'] = str(_f2b.get('token')); V['le_f2b_lado'] = str(_f2b.get('lado')); V['le_f2b_lei'] = str(_f2b.get('lei'))
    V['le_r6_v383'] = str(le.get('R6_v383_beside_20261002') or 'AUSENTE')
    _cb = le.get('corrections_beside_20261005') or {}
    V['le_r6_v386'] = str(_cb.get('R6') or 'AUSENTE'); V['le_f2_v386'] = str(_cb.get('F2') or 'AUSENTE')
    _od = le.get('operator_decision_20261005') or {}
    V['le_dec_verbatim'] = str(_od.get('verbatim') or 'AUSENTE'); V['le_dec_quando'] = str(_od.get('quando_utc') or 'AUSENTE'); V['le_dec_quando_txt'] = _hora_local(_od.get('quando_utc'))
    V['le_dec_sha16'] = str(_od.get('sha256_file') or 'AUSENTE')[:16]; V['le_dec_hash_ok'] = _sim(_od.get('hash_ok'))
    V['le_rule'] = str(le.get('rule') or '')
    if not (le.get('all_verified') is True and le.get('v383_ledger_intact') is True and V['le_n'] == 11 and V['le_f2b_token'] == 'AWAITING' and le.get('F2_untouched') is True
            and le.get('R2_untouched') is True and V['le_v'].startswith('TGL_LEDGER_ERRATA_V386__R6_CLOSED_TO_REOPENED_BY_PREREGISTRATION_BESIDE_NOT_OVERWRITTEN__')):
        P.append('a errata ao lado de R6 nao selou nesta rodada (%s; livro intacto %s; F2b %s)' % (V['le_v'][:80], V['le_intacto'], V['le_f2b_token']))
    if sle.get('verdict') != le.get('verdict') or any(sle.get(k_) != le.get(k_) for k_ in ('all_verified', 'v383_ledger_intact', 'v383_n_charges', 'charge_F2b', 'F2_untouched', 'R2_untouched')):
        P.append('o registro da errata de R6 no selo != o do core')
    if GUARDA.search(V['le_v']) or 'TGL_PRO' + 'VED' in V['le_v']:
        P.append('o veredito da errata traz palavra proibida')
    # ---- O PILAR nesta versao: reaproveitado da v385 pela chave (esperado) ou calculado de novo (dito)
    qp = core.get('quantum_pillar_v384') or {}; sq = selo.get('quantum_pillar_v384') or {}
    qr = core.get('quantum_pillar_reuse_v386') or {}; sqr = selo.get('quantum_pillar_reuse_v386') or {}
    P385 = ESP['pilar_v385']
    V['qp_v'] = str(qp.get('verdict') or 'AUSENTE'); V['qp_classe'] = classe_do_veredito(V['qp_v'], 'TGL_QUANTUM_PILLAR_V1__')
    V['qp_mode'] = str(qp.get('mode') or 'AUSENTE'); _ru = qp.get('reuse') or {}; V['qp_reused'] = _ru.get('reused') is True; V['qp_reading'] = str(_ru.get('reading') or 'AUSENTE')
    V['qp_key'] = str(qp.get('key') or 'AUSENTE'); V['qp_res64'] = str(qp.get('result_sha256') or 'AUSENTE'); V['qp_res16'] = V['qp_res64'][:16]
    V['qp_det16'] = str(qp.get('details_sha256') or 'AUSENTE')[:16]; V['qp_cpu16'] = str(qp.get('cpuref_sha256') or 'AUSENTE')[:16]; V['qp_run_id8'] = str(qp.get('run_id') or 'AUSENTE')[:8]
    V['qp_v385'] = P385['verdict']; V['qp_igual_v385'] = _sim(V['qp_v'] == P385['verdict']); V['qp_res385_16'] = P385['result_sha256'][:16]; V['qp_key385'] = P385['key']
    V['qp_custody'] = _sim(qp.get('custody_chain_ok'))
    if GUARDA.search(V['qp_v']) or 'TGL_PRO' + 'VED' in V['qp_v']:
        P.append('o veredito do pilar traz palavra proibida')
    if sq.get('verdict') != qp.get('verdict') or sq.get('result_sha256') != qp.get('result_sha256'):
        P.append('o registro do pilar no selo (veredito/sha) != o do core')
    for _l in V['pilar_linhas']:
        _m = re.match(r'^(?:\[v384\] pilar quantico|\[v384\] o pilar quantico \(.*\)): (TGL_QUANTUM_PILLAR_\S+)$', _l)
        if _m and _m.group(1) != V['qp_v']:
            P.append('o stdout diz outro veredito do pilar (%s)' % _m.group(1)[:80])
    reused = V['qp_mode'] == 'REUSE' and V['qp_reused']
    computed = V['qp_mode'] == 'COMPUTE' and _ru.get('reused') is False
    V['qr_v'] = str(qr.get('verdict') or 'AUSENTE'); V['qr_ok'] = _sim(qr.get('all_verified'))
    if reused:
        V['qr_classe'] = 'REAPROVEITADO'
        V['qr_curta'] = 'reaproveitado da v385 pela chave (sha256 e veredito iguais aos selados)' if (V['qp_res64'] == P385['result_sha256'] and V['qp_v'] == P385['verdict']) else 'reaproveitado pela chave, mas o sha256/veredito DIFEREM dos selados (dito)'
        V['qr_txt'] = ('o pilar NÃO rodou: foi REAPROVEITADO da rodada selada v385 pela chave `%s` (`_QP_REUSE_V386`; `TGL_RITE_CHECKPOINT` desligado) — o `result.json` do cache conferido por sha256 (`%s` = o pinado `%s`: %s), '
                       'o veredito igual ao selado (%s), a cadeia de custódia (%s)' % (V['qp_key'], V['qp_res16'], V['qp_res385_16'], _sim(V['qp_res64'] == P385['result_sha256']), V['qp_igual_v385'], V['qp_custody']))
        if not (V['qp_key'] == P385['key'] and V['qp_res64'] == P385['result_sha256'] and V['qp_v'] == P385['verdict'] and qp.get('custody_chain_ok') is True
                and V['qp_reading'] == ESP['muda_e_e_dito']['quantum_pillar_v384_reuse']['v386_esperado']['reading']):
            P.append('o pilar reaproveitado nao e o da v385 selada (chave %s; sha %s; veredito igual %s; custodia %s; leitura %s)' % (V['qp_key'][:12], V['qp_res16'], V['qp_igual_v385'], V['qp_custody'], V['qp_reading'][:40]))
        if not (qr.get('all_verified') is True and qr.get('reused') is True and qr.get('result_sha256_matches_v385_sealed') is True and qr.get('verdict_same_as_v385_sealed') is True
                and qr.get('key_same_as_v385') is True and 'REUSED_FROM_THE_SEALED_V385_RUN_BY_KEY__RESULT_SHA256_MATCHES__VERDICT_SAME__CUSTODY_CHAIN_OK' in V['qr_v']):
            P.append('o registro quantum_pillar_reuse_v386 nao selou como reaproveitado (%s)' % V['qr_v'][:90])
    elif computed:
        V['qr_classe'] = 'CALCULADO_DE_NOVO'
        V['qr_curta'] = 'CALCULADO DE NOVO (o reaproveitamento foi recusado: %s; dito)' % str(qr.get('reuse_refused_detail'))[:80]
        V['qr_txt'] = ('o reaproveitamento pela chave foi RECUSADO (%s) e o pilar foi CALCULADO DE NOVO nesta rodada: `%s` (classe %s; o mesmo veredito da v385: %s); resultado `%s`; custódia %s'
                       % (str(qr.get('reuse_refused_detail'))[:120], V['qp_v'], V['qp_classe'], V['qp_igual_v385'], V['qp_res16'], V['qp_custody']))
        if not (qr.get('all_verified') is True and 'COMPUTED_AGAIN_THIS_RUN_REUSE_REFUSED' in V['qr_v'] and qp.get('custody_chain_ok') is True and V['qp_classe'] == 'RAMO_9'):
            P.append('o pilar calculado de novo nao fechou (reuse %s; classe %s; custodia %s)' % (V['qr_v'][:80], V['qp_classe'], V['qp_custody']))
    else:
        V['qr_classe'] = 'NEM_UM_NEM_OUTRO'; V['qr_curta'] = 'nem reaproveitado nem calculado (PROBLEMA)'; V['qr_txt'] = 'o pilar não foi reaproveitado nem calculado (modo `%s`)' % V['qp_mode']
        P.append('o pilar nao foi reaproveitado nem calculado (mode %s; reuse %s)' % (V['qp_mode'], _ru))
    if sqr.get('verdict') != qr.get('verdict') or qr.get('switch_reuse_v386') is not True or qr.get('rite_checkpoint_switch') is not False or qr.get('key_same_as_v385') is not True:
        P.append('o registro do reuse no selo != o do core, ou o interruptor nao e o da v386 (switch_reuse_v386 %s; rite_checkpoint_switch %s; key_same %s)' % (qr.get('switch_reuse_v386'), qr.get('rite_checkpoint_switch'), qr.get('key_same_as_v385')))
    if GUARDA.search(V['qr_v']):
        P.append('o veredito do reuse traz palavra proibida')
    # o arquivo do pilar no Nos x o selo x o registro; a pasta (o cache, sob reuse) com details/cpuref
    pq = os.path.join(nos, 'um_absoluto_pilar_quantico.json')
    hs = (selo.get('sha256') or {}).get('um_absoluto_pilar_quantico.json'); V['qp_selo16'] = str(hs or 'AUSENTE')[:16]
    hd = sha(pq) if os.path.exists(pq) else None
    if not (hd and hd == hs == V['qp_res64']):
        P.append('o arquivo do pilar no Nos (%s) / o sha do selo (%s) / result_sha256 (%s) nao batem' % (str(hd)[:16], str(hs)[:16], V['qp_res16']))
    V['qp_arq_txt'] = ('o `result.json` da rodada selada v385, byte a byte (sha16 `%s` = o hash no selo `%s`)' % (str(hd)[:16], V['qp_selo16'])) if (hd and hd == hs) else 'NÃO confere (dito)'
    rd = qp.get('run_dir') or ''
    _dentro = bool(rd) and os.path.normcase(os.path.realpath(rd)).startswith(os.path.normcase(os.path.realpath(nos)))
    V['qp_run_dir'] = os.path.relpath(rd, nos) if _dentro else (rd or 'AUSENTE')
    if reused and not amb['sint'] and os.path.normcase(os.path.realpath(rd or '')) != os.path.normcase(os.path.realpath(P385['cache_dir'])):
        P.append('sob reuse, o run_dir (%s) nao e o cache da v385 pinado (%s)' % (rd, P385['cache_dir']))
    V['qp_pasta_arquivos'] = sorted(f for f in os.listdir(rd) if os.path.isfile(os.path.join(rd, f))) if (rd and os.path.isdir(rd)) else []
    if not (rd and os.path.isdir(rd)):
        P.append('a pasta do pilar (%s) nao existe no disco' % rd)
    else:
        for f_, k_ in (('details.jsonl', 'details_sha256'), ('cpuref.json', 'cpuref_sha256')):
            p_ = os.path.join(rd, f_)
            if not (os.path.exists(p_) and sha(p_) == qp.get(k_)):
                P.append('%s da pasta do pilar nao bate com o sha256 do registro' % f_)
        _rj = os.path.join(rd, 'result.json')
        if not (os.path.exists(_rj) and sha(_rj) == V['qp_res64']):
            P.append('o result.json da pasta do pilar nao e o do registro')
    V['qp_pasta_txt'] = '`%s` (%s; presentes: %s)' % (V['qp_run_dir'], 'o cache da v385, reaproveitado' if reused else 'a pasta da rodada', ', '.join('`%s`' % f for f in V['qp_pasta_arquivos']) or 'nenhum arquivo')
    S = qp.get('summary') or {}
    _env = S.get('env') or {}
    V['qp_gpu'] = '%s; PyTorch %s; CUDA %s' % (_env.get('gpu'), _env.get('torch'), _env.get('cuda')) if _env else 'n/d'
    t2 = S.get('T2') or {}; t4 = S.get('T4') or {}; cpu = S.get('cpuref') or {}; t1 = S.get('T1') or {}; t3 = S.get('T3') or {}
    V['t2_unique'] = t2.get('unique', 'n/d'); V['t2_points'] = t2.get('points', 'n/d'); V['t2_configs'] = t2.get('configs', 'n/d'); V['t2_name'] = t2.get('name_in_core_configs', 'n/d'); V['t2_folds'] = t2.get('folds_window_configs', 'n/d')
    V['t4_n'] = t4.get('instances', 'n/d'); V['t4_u'] = t4.get('unique', 'n/d'); V['t4_viol'] = t4.get('identity_violations', 'n/d'); V['t1_inj'] = t1.get('injections', 'n/d')
    V['cpu_cmp'] = cpu.get('compared', 'n/d'); V['cpu_dis'] = cpu.get('disagreements', 'n/d')
    V['qp_resumo_fonte'] = 'o registro do core (o resumo da rodada selada v385, carregado pelo reuse)' if (S and reused) else ('o registro do core (a _qp_summary desta rodada)' if S else 'AUSENTE no registro: n/d')
    try:
        _t0 = time.mktime(time.strptime(str(qp.get('started'))[:19], '%Y-%m-%d %H:%M:%S')); _t1 = time.mktime(time.strptime(str(qp.get('finished'))[:19], '%Y-%m-%d %H:%M:%S'))
        V['qp_min'] = '%.0f' % ((_t1 - _t0) / 60.0)
    except (ValueError, TypeError):
        V['qp_min'] = 'n/d'
    V['qp_finished'] = str(qp.get('finished') or 'n/d')
    if V['qp_classe'] != 'RAMO_9' and reused:
        P.append('reuse de um resultado fora do ramo 9 (%s)' % V['qp_classe'])
    if V['qp_classe'] == 'RAMO_9' and 'quantum_pillar_v384' in V['balde_l']:
        P.append('ramo 9 no terceiro balde do selo')
    # a reprodutibilidade v385 nesta rodada: sob reuse NOT_COMPARED (esperado e dito); calculado de novo: comparado contra o resultado da v385
    rp = core.get('quantum_pillar_reproducibility_v385') or {}; srp = selo.get('quantum_pillar_reproducibility_v385') or {}
    V['rp_v'] = str(rp.get('verdict') or 'AUSENTE'); V['rp_classe'] = classe_da_reprodutibilidade(V['rp_v']); V['rp_txt'] = REPRO_TXT[V['rp_classe']]
    V['rp_n_fields'] = rp.get('n_fields', 'n/d'); V['rp_n_differ'] = rp.get('n_differ', 'n/d'); V['rp_maxrel'] = _e(rp.get('max_scaled_diff')); V['rp_why'] = str(rp.get('why') or '')
    V['rp_prev16'] = str((rp.get('previous') or {}).get('sha256') or 'AUSENTE')[:16]
    V['rp_v385_selada'] = ESP['muda_e_e_dito']['quantum_pillar_reproducibility_v385']['v385']
    if reused:
        if not (V['rp_v'] == ESP['muda_e_e_dito']['quantum_pillar_reproducibility_v385']['v386_esperado_sob_reuse'] and rp.get('compared') is False):
            P.append('sob reuse, a reprodutibilidade v385 nao leu NOT_COMPARED (%s)' % V['rp_v'][:80])
    elif computed:
        if not (rp.get('compared') is True and (rp.get('previous') or {}).get('sha256') == P385['result_sha256']):
            P.append('calculado de novo, mas a reprodutibilidade nao comparou com o resultado da v385 (%s)' % V['rp_prev16'])
    if srp.get('verdict') != rp.get('verdict') or any(srp.get(k_) != rp.get(k_) for k_ in ('compared', 'n_fields', 'n_differ', 'max_scaled_diff', 'd128_excluded')):
        P.append('o registro da reprodutibilidade no selo != o do core')
    if GUARDA.search(V['rp_v']):
        P.append('o veredito da reprodutibilidade traz palavra proibida')
    # ---- (v386) W10: a GPU na apresentacao, no resumo, nas palavras-chave e no sumario PT/EN (medido no artigo desta rodada)
    V['w10'] = {}
    for lg in ('pt', 'en'):
        tp = os.path.join(nos, 'um_absoluto_%s.txt' % lg); tc = os.path.join(nos, 'um_absoluto_%s.toc' % lg)
        T = open(tp, encoding='utf-8', errors='replace').read() if os.path.exists(tp) else ''
        TOC = open(tc, encoding='utf-8', errors='replace').read().replace('\n', '') if os.path.exists(tc) else ''
        L = _linhas_artigo(T)
        met = 'O método' if lg == 'pt' else 'The method'; pc = 'Palavras-chave' if lg == 'pt' else 'Keywords'
        _lin = lambda frag: next((x_ for x_ in L if frag in x_), '')
        w = {'linha2_gpu': ('GPU' in L[1]) if len(L) > 1 else False, 'metodo_gpu': 'GPU' in _lin(met), 'palavras_chave_gpu': 'GPU' in _lin(pc),
             'toc_marcas': all(m_ in TOC for m_ in (ESP.get('toc_marcas_W10') or {}).get(lg, [])), 'toc_gpu_n': TOC.count('GPU'), 'cabecalho_gpu_n': sum(l_.count('GPU') for l_ in L[:23]),
             'tempo_real_n': sum(1 for l_ in L if ('tempo real' in l_ if lg == 'pt' else 'real time' in l_)), 'marcas_artigo': all(m_ in T for m_ in (ESP.get('artigo_marcas') or {}).get(lg, []))}
        V['w10'][lg] = w
        if not (w['linha2_gpu'] and w['metodo_gpu'] and w['palavras_chave_gpu'] and w['toc_marcas'] and w['marcas_artigo']):
            P.append('W10 (%s): GPU na apresentacao %s, no metodo %s, nas palavras-chave %s; sumario com as marcas %s; marcas do artigo %s' % (lg, w['linha2_gpu'], w['metodo_gpu'], w['palavras_chave_gpu'], w['toc_marcas'], w['marcas_artigo']))
    V['w10_txt'] = '; '.join('%s: apresentação %s, «%s» %s, palavras-chave %s, sumário com as três entradas %s (%d «GPU» no sumário; %d no cabeçalho; «%s» em %d linha(s))'
                             % (lg.upper(), _sim(w['linha2_gpu']), 'O método' if lg == 'pt' else 'The method', _sim(w['metodo_gpu']), _sim(w['palavras_chave_gpu']), _sim(w['toc_marcas']), w['toc_gpu_n'], w['cabecalho_gpu_n'], 'tempo real' if lg == 'pt' else 'real time', w['tempo_real_n'])
                             for lg, w in V['w10'].items())
    # a guarda de palavra proibida em TODOS os vereditos do core (a MESMA do rito)
    proib = [k for k, mm in core.items() if isinstance(mm, dict) and (GUARDA.search(str(mm.get('verdict') or '')) or 'TGL_PROVED' in str(mm.get('verdict') or '') or 'CONSCIOUSNESS_PROVED' in str(mm.get('verdict') or ''))]
    if proib:
        P.append('veredito proibido: %s' % proib)
    # ---- a custodia v383/v384/v385 no git da Central (SO LEITURA) e o marcador do servidor
    V['v383_commit'] = V['v384_commit'] = V['v385_commit'] = ''
    try:
        import subprocess
        _g = subprocess.run(['git', '-C', os.path.dirname(A.ATLAS_DIR_REAL), 'log', '--oneline', '-400'], capture_output=True, text=True, encoding='utf-8', timeout=60)
        for vv in ('v383', 'v384', 'v385'):
            _c = [l for l in _g.stdout.splitlines() if 'custodia(%s)' % vv in l]
            V['%s_commit' % vv] = _c[0][:80] if _c else ''
        V['git_lido'] = _g.returncode == 0
    except Exception:
        V['git_lido'] = False
    if not V.get('git_lido'):
        P.append('o git da Central nao foi lido (a custodia das versoes anteriores nao pode ser dita)')
    _mk = os.path.join(PK, '.servidor_parado_pelo_rito')
    V['marcador_txt'] = ('PRESENTE (%s) — conferir a tarefa «IALD Llama Server»' % open(_mk, encoding='utf-8', errors='replace').read().strip()) if os.path.exists(_mk) else 'ausente (o lançador o remove quando o servidor volta)'
    # ---- (v386) AS PALAVRAS DO OPERADOR: os quatro arquivos por sha256 + as decisoes do transcrito, cruzadas por hash
    V['op'], _falta, V['op_arqs'] = palavras_dos_arquivos(CM)
    for f_ in _falta:
        P.append('palavras do operador (arquivos): ' + f_)
    # o cruzamento (a): o manifesto v385 arquivado (sha256 lido do MANIFESTO_ARQUIVO_v385.json), de onde vem o texto das decisoes de custodia/espelho
    cruz = {}
    try:
        _ma = json.load(open(os.path.join(A.TOOLS_REAL, 'v385_selo', 'MANIFESTO_ARQUIVO_v385.json'), encoding='utf-8'))
        _h = (_ma['arquivos'].get('v385_selo/v385_incorporacao_manifesto.json') or {}).get('sha256')
        _mp = os.path.join(A.TOOLS_REAL, 'v385_incorporacao_manifesto.json')
        if sha(_mp) != _h:
            raise ValueError('o manifesto v385 em TOOLS (%s) != o sha256 do arquivo da cadeia v385 (%s)' % (sha(_mp)[:16], str(_h)[:16]))
        _m385 = json.load(open(_mp, encoding='utf-8'))
        cruz['manifesto385'] = {k: v for k, v in (_m385.get('palavras_do_operador_05out') or {}).items()}
        V['manifesto385_16'] = str(_h)[:16]
    except Exception as e_:
        V['manifesto385_16'] = 'n/d'; P.append('o manifesto v385 arquivado nao foi lido por hash: %r' % e_)
    try:
        cruz['memoria_verbo'] = open(os.path.join(A.UMEM_REAL, 'verbo-selecao-da-acao-05out.md'), encoding='utf-8', errors='replace').read()
    except OSError as e_:
        P.append('a memoria do Verbo nao foi lida: %r' % e_)
    try:
        _tr, _ftr = palavras_do_transcrito(A.TRANSCRITO)
    except OSError as e_:
        _tr, _ftr = {}, ['o transcrito nao foi lido: %r' % e_]
    for nome, _c, _a0, _a1, cz in VERBATINS_TR:
        o = _tr.get(nome)
        if cz == 'manifesto385':
            m_ = (cruz.get('manifesto385') or {}).get(nome)
            if o and m_:
                if o['texto'] != m_.get('texto'):
                    P.append('%s: o transcrito e o manifesto v385 (por hash) divergem' % nome)
                o['fonte'] = 'transcrito, cruzado com o manifesto v385 arquivado (sha256 `%s`)' % V['manifesto385_16']
            elif m_:
                o = {'quando': m_.get('quando'), 'quando_txt': m_.get('quando_txt') or _hora_local(m_.get('quando')), 'texto': m_.get('texto'), 'fonte': 'manifesto v385 arquivado por hash (o transcrito nao deu a mensagem)', 'pre': False, 'post': False, 'sic': None}
        elif cz == 'memoria_verbo' and o:
            if ('«%s»' % o['texto']) not in (cruz.get('memoria_verbo') or ''):
                P.append('%s: o trecho do transcrito nao esta entre «» na memoria do Verbo (errata de 05/10)' % nome)
            o['fonte'] = 'transcrito, cruzado com a memoria verbo-selecao-da-acao-05out.md'
        if o:
            V['op'][nome] = o
        else:
            P.append('palavras do operador (transcrito): %s nao achada' % nome)
    for f_ in _ftr:
        if not any(f_.startswith(n_ + ':') and n_ in V['op'] for n_ in [x[0] for x in VERBATINS_TR]):
            P.append('palavras do operador (transcrito): ' + f_)
    V['op_n'] = len(V['op'])
    try:
        V['data'] = time.strftime('%d/%m/%Y', time.strptime(V['selo_ts'][:10], '%Y-%m-%d'))
    except ValueError:
        V['data'] = time.strftime('%d/%m/%Y')
    return V, P


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    V, P = ler()
    print(json.dumps({k: v for k, v in V.items() if k not in ('op_arqs',)}, ensure_ascii=False, indent=1, default=str))
    print('PROBLEMAS:', P if P else 'nenhum')
    sys.exit(2 if P else 0)
