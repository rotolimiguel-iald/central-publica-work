# -*- coding: utf-8 -*-
# LEITURA da rodada v384 -- SO LEITURA (nao executa codigo do um.py, do pacote nem do trabalhador). Todo numero, hash e veredito sai daqui, LIDO do artefato
# (o core, o selo, o stdout, o registro do pilar no core E o arquivo de resultado da pasta da rodada -- result.json, ou result_partial.json no PARCIAL --,
# o MARCADOR do pilar no Nos quando nao ha resultado, o pre-registro V1 na pasta permanente da Bancada, o conferidor, o pacote v384, os backups de BYTES
# da v383 selada), nunca digitado.
# Usado por superficies_v384.py, manifesto_v384.py, patch_arvore_indice_v384.py, handoff_v384.py, registrar_resultado_v384.py, compactar_memory_para_v384.py.
# PROBLEMAS (lista P) param a cadeia: o rito nao limpo, o conferidor reprovado (fora do aceite nomeado), o gate mudou, a escada != ESPERADOS, um modulo da
# v383 mudou de all_verified (comparado ao estado SELADO da v383), palavra proibida, um hash que nao bate (o um.py, o pilar no selo x out_file_sha256 x
# disco, o resultado x o registro, um arquivo que o resultado amarra por sha256), o veredito do pilar fora do prefixo do pre-registro, e todo fato da
# custodia do pilar que o PROPRIO artefato nao explica.
# O RESULTADO do pilar NAO e' problema, em classe nenhuma: ramo 9 (com os negativos), PARCIAL (le-se o result_partial.json, sem .sha256 por construcao),
# NOT_RUN (recusa do um.py, sem linha de lancamento; falha fatal ou recusa do trabalhador, com result.json sem details/cpuref amarrados; sem arquivo de
# resultado, com o MARCADOR no Nos), RESULTS_VOID, motor que falhou, fase que falhou, custodia incompleta. Cada fato que o artefato explica (o fatal, a
# recusa, o parcial, o error_code da CPU, o marcador) vai aos negativos DITOS (V['qp_neg_extra_l']), nao a P; no RAMO 9 a exigencia segue estrita.
# Quem para a cadeia nessas classes e' o CONFERIDOR congelado (que exige o ramo 9): a gerencia, se decidir registrar o negativo como resultado, roda de novo
# com V384_ACEITO_PILAR_NAO_CONCLUIDO=<sha16 da conferencia_rito_v384.json>; a leitura confere que a conferencia e' ESSA e que TODAS as falhas sao itens do
# pilar, e os textos dizem o aceite. Ensaiado classe a classe, de ponta a ponta (variantes_pilar_v384.py -> testar_formatos_v384.py e ensaio_guardas_v384.py).
import os, re, json, glob, hashlib, time, datetime
import ambiente_v384 as A

HERE = os.path.dirname(os.path.abspath(__file__))
PK = A.PK
NOS_REAL = A.NOS_REAL
FINAL_RE = re.compile(r'^\[selo\] colapso tipado: ')
TRAILER_RE = re.compile(r'^(exit=\d+|rc=\d+|RITO_RC=\S+|inicio |fim )')
GUARDA = re.compile('(?<!NOT_)(?<!UN)' + 'CONF' + 'IRMED|(?<!AP)PRO' + 'VED_BY')
# os itens do conferidor congelado que falam SO do pilar (o resto -- gate, escada, vereditos, selo, artigo, md -- nunca e' aceito como falha)
PILAR_ITENS = ("o pilar RODOU nesta rodada", "o veredito do pilar e' da arvore congelada", "a cadeia de custodia do pilar confere",
               "o resultado foi GRAVADO no cache", "o selo registra o mesmo veredito e o mesmo sha256 do resultado", "o beta do trabalhador e' o do core",
               "o resultado do pilar esta no Nos e no hash do selo", "o terceiro balde da custodia de sentido existe e esta vazio",
               "details.jsonl e cpuref.json da rodada batem")
CLASSE_TXT = {'RAMO_9': 'o ramo 9 da árvore congelada: o cálculo completou, os controles falharam como exigido, as identidades valem e a referência na CPU concorda',
              'PARCIAL': 'resultado PARCIAL (o trabalhador parou antes do fim) — computação não concluída',
              'CUSTODIA_INCOMPLETA': 'a cadeia de custódia do pilar não fechou — resultado não válido, computação não concluída',
              'NAO_RODOU': 'o pilar NÃO rodou (recusa ou falha fora das fases) — computação não concluída',
              'ANULADO': 'resultado ANULADO pela própria árvore (RESULTS_VOID): as fases chegaram ao fim e o resultado não vale — computação não concluída',
              'MOTOR_FALHOU': 'o autoteste do motor (E1–E8) falhou — nada se calculou',
              'FASE_FALHOU': 'uma fase do cálculo falhou — resultados incompletos',
              'DESCONHECIDO': 'veredito fora da árvore pré-registrada'}
# as causas, lidas do TOKEN do veredito (o que cada token diz, na arvore congelada do trabalhador -- derive_verdict -- e no runtime do um.py)
NOT_RUN_TXT = {'NO_RESULT_FILE': 'o trabalhador não deixou arquivo de resultado (nem o parcial)',
               'WORKER_FATAL': 'falha fatal do trabalhador', 'PARENT_GONE': 'o trabalhador viu o processo do um.py desaparecer e parou',
               'GPU_UNAVAILABLE': 'a GPU não estava disponível para o trabalhador',
               'SPEC_HASH_MISMATCH': 'o trabalhador recusou: a especificação recebida não tem o hash congelado',
               'WORKER_HASH_MISMATCH': 'o trabalhador recusou: o seu próprio sha256 não é o congelado',
               'MISSING_ARGUMENTS': 'o trabalhador recusou: argumentos ausentes',
               'SPEC_HASH_MISMATCH_IN_UM_PY': 'o um.py recusou antes de lançar: a especificação embutida não tem o hash congelado',
               'LAUNCH_FAILED': 'o lançamento do trabalhador falhou', 'FINISH_FAILED': 'a leitura do resultado pelo um.py falhou',
               'NO_VERDICT': 'o resultado não trouxe veredito'}
PARCIAL_TXT = {'WORKER_STOPPED_BY_TIMEOUT': 'o prazo do um.py encerrou o trabalhador'}


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def _aplicado():
    ps = sorted(glob.glob(os.path.join(PK, 'APLICADO_AO_CANONICO_*.json')))
    assert ps, 'APLICADO_AO_CANONICO_*.json ausente no pacote v384'
    return json.load(open(ps[-1], encoding='utf-8')), ps[-1]


def _e(x, nd=2):
    return ('%.*e' % (nd, x)) if isinstance(x, (int, float)) and x == x else 'n/d'


def _f(x, nd=2):
    return ('%.*f' % (nd, x)) if isinstance(x, (int, float)) and x == x else 'n/d'


def _pct(x):
    return ('%.0f%%' % (100.0 * x)) if isinstance(x, (int, float)) else 'n/d'


def _num(x):
    """um numero lido, na grafia brasileira (virgula decimal)."""
    return ('%g' % x).replace('.', ',') if isinstance(x, (int, float)) else 'n/d'


def _sim(x):
    """um booleano lido, em portugues (nunca o literal do Python no texto)."""
    return 'sim' if x is True else ('não' if x is False else 'não conferido nesta rodada')


def _hora_local(iso):
    """'2026-10-04T18:24:04.971Z' -> a hora LOCAL desta maquina (o fuso lido do sistema), com a UTC ao lado."""
    try:
        d = datetime.datetime.strptime(str(iso)[:19], '%Y-%m-%dT%H:%M:%S').replace(tzinfo=datetime.timezone.utc)
        l = d.astimezone(); off = l.strftime('%z')
        return '%s, hora local UTC%s%s:%s = %s UTC' % (l.strftime('%d/%m/%Y %H:%M:%S'), '−' if off[0] == '-' else '+', off[1:3], off[3:5], d.strftime('%H:%M:%S'))
    except (ValueError, TypeError, IndexError):
        return str(iso)


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


def causa_do_veredito(v, classe, R, qp):
    """A CAUSA, em prosa, tirada do token do veredito (e do detalhe que o proprio resultado/registro grava). '' quando a classe ja diz tudo."""
    if classe == 'NAO_RODOU':
        m = re.search(r'__NOT_RUN__([A-Z0-9_]+?)__(?:CUSTODY_CHAIN_INCOMPLETE__|PARTIAL_RESULT_[A-Z0-9_]+__)?GATE_UNTOUCHED', v)
        tok = m.group(1) if m else '?'
        det = R.get('fatal') or R.get('refused') or qp.get('refused') or qp.get('error')
        return NOT_RUN_TXT.get(tok, 'motivo `%s`' % tok) + (' (`%s`)' % str(det)[:160] if det else '')
    if classe == 'ANULADO':
        m = re.search(r'__INSTANCE_ERRORS_(\d+)__', v)
        if m:
            return '%s instância(s) com exceção: o motor é suspeito' % m.group(1)
        m = re.search(r'__IDENTITY_VIOLATED_(\d+)__', v)
        if m:
            return '%s violação(ões) de identidade: o motor é suspeito' % m.group(1)
        if '__CONTROL_DID_NOT_FAIL__' in v:
            return 'um controle que tinha de falhar não falhou: o instrumento está cego'
        if '__CPU_REFERENCE_NOT_COMPARABLE__' in v:
            return 'a referência na CPU não teve ponto comparável (todos perto do limiar): nem discordância, nem conferência'
        if '__CPU_REFERENCE_DISAGREES_OR_ABSENT__' in v:
            cc = R.get('cpuref_compare') or {}
            d = ('`%s`' % cc['error_code']) if cc.get('error_code') else (('%s discordância(s)' % cc['disagreements']) if isinstance(cc.get('disagreements'), int) else '')
            return 'a referência na CPU discordou ou faltou' + (' (%s)' % d if d else '')
        return ''
    if classe == 'PARCIAL':
        m = re.search(r'__PARTIAL_RESULT_([A-Z0-9_]+?)__GATE_UNTOUCHED', v); tok = m.group(1) if m else '?'
        mr = re.match(r'WORKER_DIED_RC_(\S+)$', tok)
        c = PARCIAL_TXT.get(tok) or (('o trabalhador terminou sem o resultado final (código de saída %s)' % mr.group(1)) if mr else 'motivo `%s`' % tok)
        mf = re.search(r'__PHASE_(T\d)_FAILED__', v)
        if mf:
            c += '; a árvore, sobre o parcial, diz que a fase %s não completou' % mf.group(1)
        elif '__FIVE_JUMP_GKLS__' in v:
            c += '; a árvore, sobre o parcial, deu a forma do ramo 9 — que NÃO vale como resultado completo'
        return c
    if classe == 'FASE_FALHOU':
        m = re.search(r'__PHASE_(T\d)_FAILED__', v); ph = m.group(1) if m else '?'
        er = (R.get(ph) or {}).get('error') if isinstance(R.get(ph), dict) else None
        return 'a fase %s falhou%s' % (ph, (' (`%s`)' % str(er)[:140]) if er else '')
    if classe == 'MOTOR_FALHOU':
        ch = (R.get('engine_selftest') or {}).get('checks') or []
        f = [c.get('name') for c in ch if isinstance(c, dict) and not c.get('ok')]
        return ('os autotestes que falharam: %s' % ', '.join(f)) if f else ''
    if classe == 'CUSTODIA_INCOMPLETA':
        r = []
        if qp.get('copy_to_out_error'):
            r.append('a cópia do resultado ao Nós falhou (`%s`)' % str(qp['copy_to_out_error'])[:120])
        if qp.get('result_sha_file_ok') is False:
            r.append('o result.json.sha256 não confere')
        if qp.get('verdict_rederived') != qp.get('verdict_worker'):
            r.append('o veredito rederivado difere do do trabalhador')
        if qp.get('beta_matches_core') is False:
            r.append('o β do resultado não é o do core bit a bit')
        return '; '.join(r)
    return ''


def tokens_ramo9(v):
    """Os tokens do ramo 9 (a forma fixada no pre-registro, item 9 da arvore)."""
    t = {}
    m = re.search(r'__ATTRACTOR_UNIQUE_(?:ALL_(\d+)|(\d+)_OF_(\d+))_ON_THE_GRID__', v)
    t['attr'] = (int(m.group(1)), int(m.group(1))) if (m and m.group(1)) else ((int(m.group(2)), int(m.group(3))) if m else None)
    m = re.search(r'__T1_INSTRUMENT_(RECOVERS_INJECTED_LAW_BLIND|DOES_NOT_RECOVER_INJECTED_LAW)__', v); t['t1'] = m.group(1) if m else None
    m = re.search(r'__STRESS_(\d+)_INSTANCES_(\d+)_UNIQUE_ALL_IDENTITIES_CHECKED_IN_(\d+)__', v); t['stress'] = tuple(int(x) for x in m.groups()) if m else None
    m = re.search(r'__NAME_IN_CORE_(\d+)_OF_(\d+)_ON_THE_GRID__', v); t['name'] = (int(m.group(1)), int(m.group(2))) if m else None
    m = re.search(r'__FOLDS_WINDOW_(\d+)_OF_(\d+)_ON_THE_GRID__', v); t['folds'] = (int(m.group(1)), int(m.group(2))) if m else None
    m = re.search(r'__(D128_[A-Z0-9_]+?)__CPU_REFERENCE_AGREES__', v); t['d128'] = m.group(1) if m else None
    t['ctl'] = '__CONTROLS_FAILED_AS_REQUIRED__' in v; t['ids'] = '__IDENTITIES_HOLD__' in v; t['cpu'] = '__CPU_REFERENCE_AGREES__' in v
    return t


def _motivo_sem_amarra(f_, R, qp):
    """Por que o resultado NAO amarra details.jsonl / cpuref.json por sha256 -- so o que o PROPRIO artefato diz; None = nao explicado (vira PROBLEMA)."""
    if R.get('fatal'):
        return 'o trabalhador falhou antes de amarrá-lo (`%s`)' % str(R['fatal'])[:140]
    if R.get('refused'):
        return 'o trabalhador recusou antes de calcular (`%s`)' % R['refused']
    if not (R.get('engine_selftest') or {}).get('all_ok'):
        return 'o autoteste do motor falhou: nada se calculou'
    if qp.get('partial') is True:
        return 'resultado parcial: o trabalhador parou antes de amarrá-lo'
    if f_ == 'cpuref.json':
        cc = R.get('cpuref_compare') or {}
        if cc.get('error_code') or cc.get('error'):
            return 'a referência na CPU: `%s`' % (cc.get('error_code') or cc.get('error'))
    return None


def ler():
    P = []
    amb = A.ambiente()
    nos = amb['nos']
    ESP = json.load(open(os.path.join(PK, 'ESPERADOS_v384.json'), encoding='utf-8'))
    CM = json.load(open(os.path.join(PK, 'CANDIDATO_v384.json'), encoding='utf-8'))
    ap, app = _aplicado()
    V = {'nos': nos, 'aplicado_json': app, 'sint_bool': amb['sint'], 'sint': ' [SINTÉTICO — ENSAIO DA CADEIA, NÃO É O RITO]' if amb['sint'] else ''}
    res = json.load(open(os.path.join(nos, 'um_absoluto.json'), encoding='utf-8'))
    selo = json.load(open(os.path.join(nos, 'um_absoluto_selo.json'), encoding='utf-8'))
    if amb['sint'] != bool(selo.get('SINTETICO_ENSAIO_V384')):
        P.append('a marca SINTETICO do Nos (%s) e a do selo (%s) divergem' % (amb['sint'], bool(selo.get('SINTETICO_ENSAIO_V384'))))
    stp = os.path.join(nos, 'rodada_v384_stdout.txt')
    out = open(stp, encoding='utf-8', errors='replace').read()
    core = res['core']
    # ---- o um.py e a instalacao
    V['s64'] = sha(os.path.join(nos, 'um.py')); V['s16'] = V['s64'][:16]; V['umb'] = os.path.getsize(os.path.join(nos, 'um.py'))
    if str((selo.get('sha256') or {}).get('um.py', '')) != V['s64']:
        P.append('selo.sha256(um.py) != disco')
    if not (ap['um_py_novo']['sha16'] == V['s16'] == ESP['candidato_sha16'] == CM['sha16']):
        P.append('um.py do disco (%s) != o instalado (%s) / o candidato de ESPERADOS (%s) / CANDIDATO (%s)' % (V['s16'], ap['um_py_novo']['sha16'], ESP['candidato_sha16'], CM['sha16']))
    V['base16'] = ap['backups']['um.py']['sha16']
    if not (V['base16'] == ESP['origem_sha16'] == CM['base_v383_sha16']):
        P.append('a base substituida (%s) != a v383 selada de ESPERADOS/CANDIDATO (%s/%s)' % (V['base16'], ESP['origem_sha16'], CM['base_v383_sha16']))
    V['n_patches'] = len(CM.get('patches') or []); V['patches'] = ', '.join(p['id'] for p in CM.get('patches') or [])
    if [p['id'] for p in CM.get('patches') or []] != ESP['patches']:
        P.append('os patches do CANDIDATO != os de ESPERADOS')
    V['kernel_decl'] = str(CM.get('kernel') or 'AUSENTE')
    # o ensaio a seco e a fumaca (lidos do pacote: o que o texto diz deles sai daqui)
    try:
        _ens_p = os.path.join(PK, 'ensaio_a_seco_v384.json'); _ens = json.load(open(_ens_p, encoding='utf-8'))
        V['ensaio_seco'] = str(_ens.get('veredito'))
        if sha(_ens_p)[:16] != ESP.get('ensaio_sha16') or _ens.get('sha16') != CM['sha16'] or V['ensaio_seco'] != 'TUDO PASSOU':
            P.append('o ensaio a seco do pacote nao e o de ESPERADOS/do candidato ou nao passou (%s)' % V['ensaio_seco'])
    except Exception as e_:
        V['ensaio_seco'] = 'n/d'; P.append('o ensaio a seco nao foi lido: %r' % e_)
    _fu = sorted(glob.glob(os.path.join(PK, 'fumaca_v384_*', 'result.json')))
    _fuv = str(json.load(open(_fu[-1], encoding='utf-8')).get('verdict')) if _fu else 'AUSENTE'
    V['fumaca_txt'] = ('completou o caminho de código (`%s`; especificação de fumaça, nunca resultado do pilar)' % os.path.basename(os.path.dirname(_fu[-1]))) if '__FIVE_JUMP_GKLS__' in _fuv else ('NÃO completou (%s)' % _fuv[:80])
    # ---- o stdout do rito
    m = re.search(r'teoremas limpos:\s*(\d+)/(\d+)', out)
    V['teor'] = '%s/%s' % m.groups() if m else 'AUSENTE'
    if not m or m.group(1) != m.group(2):
        P.append('teoremas limpos ausente ou N != M')
    elif [int(m.group(1)), int(m.group(2))] != ESP['escada_v383']:
        P.append('a escada do stdout (%s) != a da v383 em ESPERADOS (%s): o kernel devia ser o MESMO' % (V['teor'], ESP['escada_v383']))
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
    V['rc'] = os.environ.get('V384_RC') or (mrc[-1] if mrc else 'NAO_LIDO')
    V['rcsrc'] = 'dito pela gerência (V384_RC)' if os.environ.get('V384_RC') else ('linha RITO_RC= do stdout (escrita pelo lançador rito_v384.sh)' if mrc else 'ausente')
    if V['rc'] != '0':
        P.append('rc do rito nao lido como 0 (%s)' % V['rc'])
    if mrc and os.environ.get('V384_RC') and mrc[-1] != os.environ['V384_RC']:
        P.append('V384_RC (%s) != RITO_RC do stdout (%s)' % (os.environ['V384_RC'], mrc[-1]))
    V['v384_linhas'] = [l.strip() for l in out.splitlines() if '[v384]' in l and 'em curso' not in l]
    V['n_progresso'] = sum(1 for l in out.splitlines() if '[v384] pilar quantico em curso' in l)
    mb = re.search(r'\[selo\] custodia de sentido: .*\| computacao nao concluida: (.*)$', out, flags=re.M)
    V['balde_stdout'] = mb.group(1).strip() if mb else 'AUSENTE'
    if not mb:
        P.append('a linha da custodia de sentido nao nomeia o terceiro balde (W08c)')
    hor = amb['horarios']
    hh = open(hor, encoding='utf-8').read().split() if os.path.exists(hor) else []
    V['t0'] = hh[0] if hh else 'n/d'
    V['t1'] = hh[1] if len(hh) > 1 else time.strftime('%H:%M:%S', time.localtime(os.stat(stp).st_mtime))
    V['tsrc'] = 'horários gravados pelo lançador rito_v384.sh' if len(hh) > 1 else 'fim = última modificação do stdout (o lançador não gravou o horário de fim)'
    V['tentativas'] = sorted(os.path.basename(p) for p in glob.glob(os.path.join(nos, 'rodada_v384_stdout_tentativa*.txt')))
    V['selo_ts'] = str(selo.get('timestamp'))
    ts_ap = '%s-%s-%s %s:%s:%s' % (ap['ts'][0:4], ap['ts'][4:6], ap['ts'][6:8], ap['ts'][9:11], ap['ts'][11:13], ap['ts'][13:15])
    if not (V['selo_ts'] >= ts_ap):
        P.append('o selo (%s) e anterior a instalacao da v384 (%s)' % (V['selo_ts'], ts_ap))
    # ---- o conferidor (copia byte a byte do pacote, rodada em v384_selo\conferidor)
    cdir = amb['conf_dir']
    confp = os.path.join(cdir, 'conferencia_rito_v384.json'); confo = os.path.join(cdir, 'conferir_rito_v384_stdout.txt')
    try:
        C = json.load(open(confp, encoding='utf-8')); CO = open(confo, encoding='utf-8', errors='replace').read()
    except OSError as e:
        C, CO = {}, ''; P.append('conferidor nao lido: %r' % e)
    dm = C.get('deve_mudar') or {}; npm = C.get('nao_pode_mudar') or {}
    V['conf_dm'] = '%d/%d' % (sum(1 for v in dm.values() if v), len(dm)); V['conf_np'] = '%d/%d' % (sum(1 for v in npm.values() if v), len(npm))
    V['conf16'] = sha(confp)[:16] if os.path.exists(confp) else 'AUSENTE'
    V['conf_falhas'] = [k for k, v in list(dm.items()) + list(npm.items()) if not v]
    V['servidor'] = str(C.get('servidor_depois_do_rito') or 'n/d'); V['avisos_lancador'] = len(C.get('avisos_do_lancador') or []); V['sinais'] = len(C.get('sinais_desta_rodada') or [])
    V['conf_aceite'] = ''
    if C.get('um_py_sha16') != V['s16']:
        P.append('o conferidor conferiu outro um.py (%s)' % C.get('um_py_sha16'))
    if not (C.get('tudo_bate') is True and CO.rstrip().endswith('TUDO BATE')):
        so_pilar = bool(V['conf_falhas']) and all(any(k.startswith(p) for p in PILAR_ITENS) for k in V['conf_falhas'])
        ac = os.environ.get('V384_ACEITO_PILAR_NAO_CONCLUIDO')
        if ac and ac == V['conf16'] and so_pilar:
            V['conf_aceite'] = ('o conferidor congelado reprovou SÓ itens do pilar (%d: %s); a gerência aceitou o resultado do pilar como resultado, '
                                'pela conferência `%s` nomeada (V384_ACEITO_PILAR_NAO_CONCLUIDO)' % (len(V['conf_falhas']), '; '.join(V['conf_falhas']), V['conf16']))
        else:
            P.append('conferidor NAO deu TUDO BATE para este um.py (falhas: %s%s)' % (V['conf_falhas'][:6], '; SO itens do pilar -- decisao da gerencia (V384_ACEITO_PILAR_NAO_CONCLUIDO=<sha16 da conferencia>)' if so_pilar else ''))
    # ---- o kernel e o gate (o MESMO da v383)
    kf = core.get('kernel_formalization') or {}
    V['n_flags_true'] = sum(1 for k, v in kf.items() if v is True)
    if V['n_flags_true'] != ESP['n_flags_true_v383']:
        P.append('bandeiras True do kernel %d != %d (v383)' % (V['n_flags_true'], ESP['n_flags_true_v383']))
    if {k: kf.get(k) for k in ESP['flags_gpf_gpc_v383']} != ESP['flags_gpf_gpc_v383']:
        P.append('as bandeiras gpf_/gpc_/gpi_ mudaram')
    V['termo'] = {k: kf.get(k) for k in ('gpf_H2_smooth_modular_four_frame_discharged', 'gpf_H3_local_horizon_equilibrium_discharged', 'gpi_H3_horizon_data_produced')}
    V['hvals'] = '/'.join(str(v) for v in V['termo'].values())
    lad = core.get('external_ladder') or {}
    V['esc'] = '%s/%s' % (lad.get('n_theorems_clean'), lad.get('n_theorems_expected'))
    if [lad.get('n_theorems_clean'), lad.get('n_theorems_expected')] != ESP['escada_v383']:
        P.append('a escada do core (%s) != a da v383 (%s)' % (V['esc'], ESP['escada_v383']))
    V['nax'] = len(kf.get('axiom_report') or {})
    if any('sorryAx' in a for v in (kf.get('axiom_report') or {}).values() for a in (v or [])):
        P.append('sorryAx no axiom_report')
    Vd = lambda k: str((core.get(k) or {}).get('verdict') or 'AUSENTE')
    dif = {k: (v, Vd(k)) for k, v in ESP['vereditos_v383'].items() if Vd(k) != v}
    V['n_ver'] = len(ESP['vereditos_v383']); V['n_ver_iguais'] = V['n_ver'] - len(dif)
    if dif:
        P.append('%d veredito(s) da v383 mudaram: %s' % (len(dif), list(dif)[:5]))
    V['livro'] = Vd('the_ledger_of_charges_v383')
    V['iald'] = Vd('the_iald_index')
    # (a guarda da leitura v383, 151-152) o the_iald_index selado
    if (core.get('the_iald_index') or {}).get('all_verified') is not True:
        P.append('the_iald_index nao selado (all_verified != True)')
    V['qg'] = str(selo.get('qg_closure_verdict'))
    if V['qg'] != ESP['qg_closure_verdict_v383']:
        P.append('o gate MUDOU (%s)' % V['qg'])
    qg = core.get('qg_closure') or {}
    V['n18'] = sum(1 for fam in ('formal_flags', 'physics_flags', 'experiment_flags') for v in (qg.get(fam) or {}).values() if v is True)
    if V['n18'] != 18:
        P.append('as bandeiras do gate nao sao 18/18 (%d)' % V['n18'])
    fr = (qg.get('gate') or {}).get('kernel_frontier') or {}
    V['remaining'] = ', '.join(fr.get('remaining') or []) or 'n/d'
    # (a guarda da leitura v383, 161-163) nada resta depois das citacoes da v374
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
    # ---- o selo da v384
    V['um_version'] = str(selo.get('um_version'))
    if V['um_version'] != 'v384':
        P.append('selo.um_version != v384 (%s)' % V['um_version'])
    if not all(selo.get(k) == v for k, v in ESP['selo_leituras_pinadas'].items()):
        P.append('as leituras v377-v383 do selo mudaram')
    V['qp_reading'] = str(selo.get('the_quantum_pillar_reading_v384') or 'AUSENTE')
    if V['qp_reading'] == 'AUSENTE':
        P.append('leitura the_quantum_pillar_reading_v384 ausente do selo')
    if GUARDA.search(V['qp_reading']) or 'TGL_PRO' + 'VED' in V['qp_reading']:
        P.append('a leitura v384 do selo traz palavra proibida')
    if ('PREREGISTRATION_V1_FROZEN_BY_HASH_' + ESP['spec_sha256'][:16].upper() + '_RATIFIED_BY_THE_OPERATOR') not in V['qp_reading']:
        P.append('a leitura v384 do selo nao diz o V1 congelado e ratificado pelo hash da especificacao')
    nst = selo.get('not_sealed_this_run') or {}
    V['formais'] = ', '.join(nst.get('formais') or []) or 'nenhum'
    if sorted(nst.get('formais') or []) != ESP['not_sealed_formais_v383']:
        P.append('os formais nao selados mudaram (%s)' % nst.get('formais'))
    if 'computacao_nao_concluida' not in nst:
        P.append('o terceiro balde (computacao_nao_concluida) nao existe no selo')
    V['balde_l'] = list(nst.get('computacao_nao_concluida') or [])
    V['balde'] = ', '.join(V['balde_l']) or 'nenhuma'
    if V['balde_stdout'] not in ('AUSENTE', V['balde']):
        P.append('o terceiro balde do stdout (%s) != o do selo (%s)' % (V['balde_stdout'], V['balde']))
    # ---- (a guarda da leitura v383, 147-149, ESTENDIDA) o estado SELADO da v383, pelos backups de BYTES do Nos (conferidos pelo sha16 do APLICADO): o
    # all_verified de TODO modulo da v383 igual (o kernel e' o MESMO) e o balde das recusas de dado igual -- um modulo que caia para all_verified False com
    # um veredito de recusa nao passa calado
    try:
        _bk = ap['backups']
        _cb = open(_bk['um_absoluto.json']['backup'], 'rb').read(); _sb = open(_bk['um_absoluto_selo.json']['backup'], 'rb').read()
        if hashlib.sha256(_cb).hexdigest()[:16] != _bk['um_absoluto.json']['sha16'] or hashlib.sha256(_sb).hexdigest()[:16] != _bk['um_absoluto_selo.json']['sha16']:
            raise ValueError('os backups da v383 no Nos nao batem com o sha16 do APLICADO')
        C383 = json.loads(_cb.decode('utf-8'))['core']; S383 = json.loads(_sb.decode('utf-8'))
        av383 = {k: m_.get('all_verified') for k, m_ in C383.items() if isinstance(m_, dict) and 'all_verified' in m_}
        difav = sorted(k for k, v in av383.items() if (core.get(k) or {}).get('all_verified') != v)
        V['n_av'] = len(av383); V['n_av_iguais'] = len(av383) - len(difav)
        if difav:
            P.append('%d modulo(s) da v383 mudaram de all_verified em relacao ao estado SELADO: %s' % (len(difav), difav[:6]))
        V['recusas'] = ', '.join(sorted(nst.get('recusas_de_dado') or [])) or 'nenhuma'
        if sorted(nst.get('recusas_de_dado') or []) != sorted((S383.get('not_sealed_this_run') or {}).get('recusas_de_dado') or []):
            P.append('o balde das recusas de dado mudou em relacao ao selo da v383 (%s)' % V['recusas'])
    except Exception as e_:
        V['n_av'] = V['n_av_iguais'] = 'n/d'; V['recusas'] = 'n/d'
        P.append('o estado selado da v383 (backups de bytes no Nos) nao foi lido: %r' % e_)
    _mds = [os.path.join(nos, 'um_absoluto_forma_canonica.md'), os.path.join(nos, 'um_absoluto_manifest.md')]
    _mtx = [open(p, encoding='utf-8', errors='replace').read() if os.path.exists(p) else '' for p in _mds]
    _car = all(ESP['md_carimbo'] in t and ('sha256/16 `%s`' % V['s16']) in t for t in _mtx)
    V['md_carimbo'] = 'SIM (forma canônica + manifesto)' if _car else 'NÃO'
    if not _car:
        P.append('os .md emitidos nao trazem o carimbo v384 com o sha16 do um.py do disco')
    # ---- o PRE-REGISTRO V1 (lido por bytes na pasta permanente da Bancada)
    PJb = open(A.PR_JSON, 'rb').read(); PMb = open(A.PR_MD, 'rb').read(); PJ = json.loads(PJb.decode('utf-8'))
    V['pr_id'] = str(PJ.get('id')); V['pr_json64'] = hashlib.sha256(PJb).hexdigest(); V['pr_md64'] = hashlib.sha256(PMb).hexdigest()
    V['pr_json16'] = V['pr_json64'][:16]; V['pr_md16'] = V['pr_md64'][:16]
    if not (V['pr_json64'] == ESP['prereg_sha256']['json'] == CM['prereg_sha256']['json'] and V['pr_md64'] == ESP['prereg_sha256']['md'] == CM['prereg_sha256']['md']):
        P.append('o pre-registro V1 em disco nao e o congelado (JSON %s / MD %s)' % (V['pr_json16'], V['pr_md16']))
    spec_canon = json.dumps(PJ['spec'], sort_keys=True, ensure_ascii=False, separators=(',', ':'))
    V['pr_spec64'] = hashlib.sha256(spec_canon.encode('utf-8')).hexdigest(); V['pr_spec16'] = V['pr_spec64'][:16]
    if not (V['pr_spec64'] == PJ.get('spec_sha256') == ESP['spec_sha256'] == CM['spec_sha256']):
        P.append('a especificacao do V1 (recalculada %s) nao e a congelada' % V['pr_spec16'])
    V['pr_worker64'] = str(PJ['spec'].get('worker_sha256')); V['pr_worker16'] = V['pr_worker64'][:16]
    if not (V['pr_worker64'] == ESP['worker_sha256'] == CM['worker_sha256']):
        P.append('o trabalhador do V1 nao e o de ESPERADOS/CANDIDATO')
    RAT = PJ.get('ratificacao_do_operador') or {}
    V['pr_verbatim'] = str(RAT.get('verbatim') or 'AUSENTE'); V['pr_quando'] = str(RAT.get('quando') or 'AUSENTE'); V['pr_escolha'] = str(RAT.get('escolha') or 'AUSENTE')
    V['pr_quando_txt'] = _hora_local(V['pr_quando'])
    if V['pr_verbatim'] != ((CM.get('ratificacao_do_operador') or {}).get('verbatim')) or RAT.get('spec_sha256_ratificada') != V['pr_spec64'] or RAT.get('a_especificacao_ratificada_e_a_do_rascunho') is not True:
        P.append('a ratificacao do V1 nao e a do candidato ou nao e da especificacao congelada')
    if (RAT.get('transcrito') or {}).get('de_teste') is not False:
        P.append('a ratificacao do V1 nao diz que veio do transcrito canonico (de_teste False)')
    # as ORDENS: contadas pelo NUMERO de cada ordem (o V1 guarda a ordem 1 em dois trechos da mesma mensagem), nunca pelo numero de trechos
    _ords = PJ.get('ordens_do_operador_verbatim') or []
    _nums = []
    for o in _ords:
        m_ = re.match(r'\s*(\d+)', str(o.get('n', '')))
        if m_:
            _nums.append(int(m_.group(1)))
    if len(_nums) != len(_ords):
        P.append('um trecho de ordem do V1 sem o numero da ordem')
    V['pr_ordens_ns'] = sorted(set(_nums)); V['pr_n_ordens'] = len(V['pr_ordens_ns']); V['pr_n_trechos'] = len(_ords)
    _ds = sorted({str(o.get('quando', ''))[5:7] + '/' + str(o.get('quando', ''))[8:10] for o in _ords if o.get('quando')})
    _ds = [d[3:] + '/' + d[:2] for d in _ds]
    V['pr_ordens_datas'] = (', '.join(_ds[:-1]) + ' e ' + _ds[-1]) if len(_ds) > 1 else (_ds[0] if _ds else 'n/d')
    _anos = sorted({str(o.get('quando', ''))[:4] for o in _ords if o.get('quando')})
    V['pr_ordens_datas'] += ('/' + '-'.join(_anos)) if _anos else ''
    ev = PJ.get('evidencias') or []; ev_ok = 0
    for e in ev:
        q = e.get('copia_permanente')
        if q and os.path.exists(q) and sha(q) == e.get('sha256'):
            ev_ok += 1
    V['pr_ev'] = '%d/%d' % (ev_ok, len(ev))
    if ev_ok != len(ev) or not ev:
        P.append('evidencias do V1 que nao batem com o sha256 gravado: %d de %d' % (len(ev) - ev_ok, len(ev)))
    import stat as _st
    V['pr_so_leitura'] = all(not (os.stat(p).st_mode & _st.S_IWRITE) for p in (A.PR_JSON, A.PR_MD))
    V['pr_so_leitura_txt'] = _sim(V['pr_so_leitura'])
    try:
        CC = json.load(open(os.path.join(PK, 'conferir_congelamento_v384_resultado.json'), encoding='utf-8'))['result']
        V['pr_conf'] = '; '.join('%s: %s' % (L['lente'], L['resultado']['veredito']) for L in CC['lentes'])
    except Exception as e_:
        V['pr_conf'] = 'n/d'; P.append('a conferencia do congelamento nao foi lida: %r' % e_)
    _orc = PJ.get('orcamento_estimado') or {}
    V['pr_orc_min'] = _f(_orc.get('total_min'), 1); V['pr_orc_margem'] = _f(_orc.get('total_com_margem_min'), 1)
    V['pr_prefixo'] = str(PJ['spec'].get('id')) + '__'
    _crit_t1 = ((PJ['spec'].get('T1') or {}).get('pass') or {})
    try:
        _D = json.load(open(os.path.join(PK, 'disposicoes_afericoes_v384.json'), encoding='utf-8'))
        V['n_afer'] = len([k for k in _D if re.fullmatch(r'passada\d+', k)])
    except Exception:
        V['n_afer'] = 'n/d'
    # ---- O PILAR: o registro do core, o do selo, o arquivo do pilar no Nos, a pasta da rodada e o arquivo de resultado dela
    qp = core.get('quantum_pillar_v384') or {}; sq = selo.get('quantum_pillar_v384') or {}
    NEG_EXTRA = []   # fatos desta rodada que o PROPRIO artefato explica (ditos pela gerencia, ao lado; nunca problema)
    if not qp:
        P.append('o core nao tem a chave quantum_pillar_v384')
    if not sq:
        P.append('o selo nao tem o registro quantum_pillar_v384')
    V['qp_v'] = str(qp.get('verdict') or 'AUSENTE')
    if GUARDA.search(V['qp_v']) or 'TGL_PRO' + 'VED' in V['qp_v']:
        P.append('o veredito do pilar traz palavra proibida')
    if not V['qp_v'].startswith(V['pr_prefixo']):
        P.append('o veredito do pilar (%s) nao comeca com o prefixo do pre-registro (%s)' % (V['qp_v'][:60], V['pr_prefixo']))
    V['qp_classe'] = classe_do_veredito(V['qp_v'], V['pr_prefixo'])
    nao9 = V['qp_classe'] != 'RAMO_9'
    if sq.get('verdict') != qp.get('verdict') or sq.get('result_sha256') != qp.get('result_sha256'):
        P.append('o registro do pilar no selo (veredito/sha) != o do core')
    for _l in V['v384_linhas']:
        _m = re.match(r'^(?:\[v384\] pilar quantico|\[v384\] o pilar quantico \(.*\)): (TGL_QUANTUM_PILLAR_\S+)$', _l)
        if _m and _m.group(1) != V['qp_v']:
            P.append('o stdout diz outro veredito do pilar (%s)' % _m.group(1)[:80])
    for k in ('mode', 'key', 'run_id', 'run_dir', 'result_sha256', 'details_sha256', 'cpuref_sha256', 'out_file_sha256', 'worker_sha256', 'spec_sha256_in_result',
              'custody_chain_ok', 'all_verified', 'beta_matches_core', 'partial', 'timed_out', 'worker_rc', 'verdict_worker', 'verdict_rederived', 'started', 'finished', 'beta_hex',
              'refused', 'copied_to_out', 'copy_to_out_error', 'out_marker_error', 'out_file_removed', 'out_file_remove_error', 'result_sha_file_ok', 'summary_error', 'error'):
        V['qp_' + k] = qp.get(k)
    V['qp_beta_txt'] = _sim(qp.get('beta_matches_core'))
    V['qp_key_txt'] = str(qp.get('key') or 'n/d')
    # o LANCAMENTO: a linha do stdout; so a recusa do PROPRIO um.py (antes do Popen: SPEC_HASH_MISMATCH_IN_UM_PY / LAUNCH_FAILED) dispensa a linha
    _lancou = any(re.match(r'^\[v384\] pilar quantico: (o trabalhador da GPU foi lancado|REAPROVEITADO)', l) for l in V['v384_linhas'])
    if qp.get('refused'):
        V['qp_lanc_txt'] = 'o trabalhador NÃO foi lançado: o um.py recusou antes (`%s`)' % str(qp['refused'])[:160]
        if V['qp_classe'] != 'NAO_RODOU':
            P.append('o registro traz recusa do um.py (%s), mas o veredito nao e NOT_RUN' % str(qp['refused'])[:80])
    elif _lancou:
        V['qp_lanc_txt'] = 'o trabalhador foi lançado (a linha do stdout)'
    else:
        V['qp_lanc_txt'] = 'AUSENTE'
        P.append('o stdout nao registra o lancamento (ou o reaproveitamento) do pilar, e o registro nao traz recusa do um.py')
    V['qp_res16'] = str(qp.get('result_sha256') or 'AUSENTE')[:16]; V['qp_det16'] = str(qp.get('details_sha256') or 'AUSENTE')[:16]
    V['qp_cpu16'] = str(qp.get('cpuref_sha256') or 'AUSENTE')[:16]; V['qp_out16'] = str(qp.get('out_file_sha256') or 'AUSENTE')[:16]
    V['qp_run_id8'] = str(qp.get('run_id') or 'AUSENTE')[:8]
    V['qp_rederiv'] = 'igual ao do trabalhador' if (qp.get('verdict_rederived') and qp.get('verdict_rederived') == qp.get('verdict_worker')) else 'DIFERENTE ou ausente'
    # o arquivo do pilar no Nos x o selo x out_file_sha256 (o que o runtime escreveu nesta rodada): o resultado, o parcial ou o MARCADOR
    pq = os.path.join(nos, 'um_absoluto_pilar_quantico.json')
    hs = (selo.get('sha256') or {}).get('um_absoluto_pilar_quantico.json'); V['qp_selo16'] = str(hs or 'AUSENTE')[:16]
    hd = sha(pq) if os.path.exists(pq) else None
    PQ = None
    if hd and os.path.getsize(pq) < (8 << 20):
        try:
            PQ = json.loads(open(pq, 'rb').read().decode('utf-8'))
        except ValueError:
            PQ = None
    marcador = isinstance(PQ, dict) and PQ.get('marker') is True
    V['qp_arq_tipo'] = 'MARCADOR' if marcador else ('AUSENTE' if hd is None else 'RESULTADO')
    if hs in (None, 'NOT_THIS_RUN', 'MISSING_THIS_RUN'):
        if nao9 and qp.get('out_marker_error'):
            V['qp_arq_tipo'] = 'NAO_ESCRITO'
            NEG_EXTRA.append('o arquivo do pilar NÃO foi escrito nesta rodada: o marcador falhou (`%s`) e %s; o selo grava `%s` para ele' % (
                str(qp['out_marker_error'])[:120], 'o arquivo foi removido do Nós' if qp.get('out_file_removed') else
                ('a remoção também falhou (`%s`): o arquivo que está no Nós NÃO é desta rodada' % str(qp.get('out_file_remove_error'))[:120]), hs))
        else:
            P.append('o selo nao hasheia o arquivo do pilar desta rodada (%s)' % hs)
    else:
        if hs != qp.get('out_file_sha256'):
            P.append('o sha do pilar no selo (%s) != out_file_sha256 (%s)' % (str(hs)[:16], str(qp.get('out_file_sha256'))[:16]))
        if hd != hs:
            P.append('o arquivo do pilar no Nos (%s) != o sha do selo (%s)' % (str(hd)[:16], str(hs)[:16]))
    if marcador:
        if not nao9:
            P.append('ramo 9 com o MARCADOR no Nos no lugar do resultado')
        if PQ.get('verdict') != qp.get('verdict'):
            P.append('o MARCADOR do Nos diz outro veredito (%s)' % str(PQ.get('verdict'))[:80])
        V['qp_marcador_motivo'] = str(PQ.get('reason')); V['qp_marcador_ausente'] = PQ.get('result_file_absent')
    # a PASTA da rodada: a do registro; sem ela (NOT_RUN sem arquivo de resultado), a que a MARCA da rodada do marcador nomeia (glob quantum_pillar\run_*_<run8>)
    rd = qp.get('run_dir') or ''
    V['qp_pasta_fonte'] = 'o registro do core'
    _rid = qp.get('run_id') or (PQ.get('run_id') if marcador else None)
    if not rd and _rid:
        _cands = sorted(glob.glob(os.path.join(nos, 'quantum_pillar', 'run_*_' + str(_rid)[:8])))
        if len(_cands) == 1:
            rd = _cands[0]; V['qp_pasta_fonte'] = 'achada pela marca da rodada do MARCADOR (`%s`)' % str(_rid)[:8]
        elif len(_cands) > 1:
            NEG_EXTRA.append('mais de uma pasta com a marca da rodada `%s`: nenhuma é tomada como a desta rodada' % str(_rid)[:8])
    V['qp_run_id8'] = str(_rid or 'AUSENTE')[:8]
    _dentro = bool(rd) and os.path.normcase(os.path.realpath(rd)).startswith(os.path.normcase(os.path.realpath(nos)))
    V['qp_run_dir'] = os.path.relpath(rd, nos) if _dentro else (rd or 'AUSENTE')
    if qp.get('mode') == 'COMPUTE' and rd and not os.path.normcase(os.path.realpath(rd)).startswith(os.path.normcase(os.path.realpath(os.path.join(nos, 'quantum_pillar'))) + os.sep):
        P.append('o run_dir (%s) nao esta em <Nos>\\quantum_pillar' % rd)
    V['qp_pasta_arquivos'] = sorted(f for f in os.listdir(rd) if os.path.isfile(os.path.join(rd, f))) if (rd and os.path.isdir(rd)) else []
    if rd and os.path.isdir(rd):
        V['qp_pasta_txt'] = '`%s` (%s; presentes: %s)' % (V['qp_run_dir'], V['qp_pasta_fonte'], ', '.join('`%s`' % f for f in V['qp_pasta_arquivos']) or 'nenhum arquivo')
    elif rd:
        V['qp_pasta_txt'] = '`%s` (nomeada por %s, mas AUSENTE no disco)' % (V['qp_run_dir'], V['qp_pasta_fonte'])
        P.append('a pasta da rodada (%s) nao existe no disco' % rd)
    else:
        V['qp_pasta_txt'] = ('não nomeada: o um.py recusou (`%s`) e nem o registro nem o marcador trazem a marca da rodada' % str(qp.get('refused'))[:80]
                             if qp.get('refused') else 'não nomeada pelo registro nem pelo marcador')
    # o ARQUIVO DE RESULTADO da pasta da rodada (result.json; no PARCIAL, o result_partial.json que o runtime leu), conferido contra o registro
    R = {}; r64 = None
    partial = qp.get('partial') is True
    rname = 'result_partial.json' if partial else 'result.json'
    rp = os.path.join(rd, rname) if rd else ''
    V['qp_resultjson'] = 'AUSENTE (%s)' % V['qp_classe']
    if qp.get('run_dir') and os.path.exists(rp):
        rb = open(rp, 'rb').read(); R = json.loads(rb.decode('utf-8')); r64 = hashlib.sha256(rb).hexdigest()
        V['qp_resultjson'] = os.path.relpath(rp, nos) if _dentro else rp
        if r64 != qp.get('result_sha256'):
            P.append('o %s da rodada (%s) != result_sha256 do registro (%s)' % (rname, r64[:16], V['qp_res16']))
        if partial:
            # o parcial nao tem .sha256 por construcao (o trabalhador so o grava com o resultado final); o runtime o marca result_sha_file_ok False
            if qp.get('result_sha_file_ok') is not False:
                P.append('resultado parcial com result_sha_file_ok != False no registro')
            if V['qp_classe'] != 'PARCIAL':
                NEG_EXTRA.append('o resultado registrado é o PARCIAL (`result_partial.json`, sem `.sha256` por construção)')
        else:
            hp = rp + '.sha256'
            if not (os.path.exists(hp) and open(hp, encoding='ascii').read().strip() == r64):
                P.append('result.json.sha256 ausente ou diferente')
        if R.get('verdict') != qp.get('verdict_worker'):
            P.append('o veredito do %s != verdict_worker do registro' % rname)
        if R.get('run_id') != qp.get('run_id'):
            P.append('o run_id do %s != o do registro' % rname)
        if R.get('spec_sha256') != ESP['spec_sha256'] or R.get('worker_sha256') != ESP['worker_sha256']:
            if nao9 and R.get('refused') in ('SPEC_HASH_MISMATCH', 'WORKER_HASH_MISMATCH'):
                NEG_EXTRA.append('o trabalhador recusou (`%s`): a especificação ou o trabalhador não são os congelados — é a própria razão da recusa' % R['refused'])
            else:
                P.append('o %s nao e da especificacao/do trabalhador congelados' % rname)
        _bh = float(core['beta']).hex() if isinstance(core.get('beta'), float) else None
        if R.get('beta_hex') is None and nao9 and (R.get('refused') or R.get('fatal')):
            NEG_EXTRA.append('β não chegou ao resultado: o trabalhador %s antes de recebê-lo' % ('recusou' if R.get('refused') else 'falhou'))
        elif not (R.get('beta_hex') == qp.get('beta_hex') == _bh):
            P.append('beta do resultado (%s) / do registro (%s) / do core (%s) nao batem bit a bit' % (R.get('beta_hex'), qp.get('beta_hex'), _bh))
        for f_, k_ in (('details.jsonl', 'details_sha256'), ('cpuref.json', 'cpuref_sha256')):
            p_ = os.path.join(rd, f_)
            if R.get(k_) is None and qp.get(k_) is None and nao9:
                mot = _motivo_sem_amarra(f_, R, qp)
                if mot:
                    NEG_EXTRA.append('`%s` não está amarrado por sha256 no resultado (%s)' % (f_, mot))
                else:
                    P.append('%s sem sha256 no resultado, e o resultado nao diz por que' % f_)
            elif not (os.path.exists(p_) and sha(p_) == R.get(k_) == qp.get(k_)):
                P.append('%s da rodada nao bate com o sha256 do resultado/registro' % f_)
        if qp.get('copied_to_out') and hd != r64:
            P.append('o arquivo do pilar no Nos nao e o %s da rodada' % rname)
        if V['qp_classe'] == 'RAMO_9':
            if not (qp.get('verdict_rederived') == qp.get('verdict_worker') == qp.get('verdict')):
                P.append('ramo 9 com veredito rederivado/do trabalhador/registrado diferentes')
            if qp.get('custody_chain_ok') is not True or qp.get('beta_matches_core') is not True or qp.get('partial') is not False:
                P.append('ramo 9 sem a cadeia de custodia/beta/completo no registro')
            if hd != r64:
                P.append('o arquivo do pilar no Nos nao e o result.json da rodada (ramo 9)')
    elif qp.get('run_dir'):
        P.append('o %s da rodada nao existe (%s), mas o registro nomeia a pasta' % (rname, rp))
    elif V['qp_classe'] == 'RAMO_9':
        P.append('ramo 9 sem a pasta da rodada no registro')
    elif V['qp_arq_tipo'] == 'RESULTADO':
        P.append('o arquivo do pilar no Nos nao e marcador, mas o registro nao nomeia a pasta da rodada')
    elif marcador and V.get('qp_marcador_ausente') is True and any(f in V['qp_pasta_arquivos'] for f in ('result.json', 'result_partial.json')):
        NEG_EXTRA.append('a pasta da rodada tem arquivo de resultado que o marcador mediu como AUSENTE na leitura do rito: não é resultado registrado desta rodada')
    # o que o arquivo do pilar no Nos E (dito em cada classe, nunca suposto)
    if V['qp_arq_tipo'] == 'MARCADOR':
        V['qp_arq_txt'] = ('o MARCADOR desta rodada, não um resultado (sha16 `%s` = o hash no selo `%s`; motivo `%s`; arquivo de resultado ausente na leitura do rito: %s)'
                           % (str(hd)[:16], V['qp_selo16'], V['qp_marcador_motivo'], _sim(V['qp_marcador_ausente'])))
    elif V['qp_arq_tipo'] == 'NAO_ESCRITO':
        V['qp_arq_txt'] = 'NÃO escrito nesta rodada (o selo grava `%s`)' % hs
    elif V['qp_arq_tipo'] == 'RESULTADO' and r64 and hd == r64:
        V['qp_arq_tipo'] = 'PARCIAL' if partial else 'RESULTADO'
        V['qp_arq_txt'] = ('o `%s` da rodada, byte a byte%s (sha16 `%s` = o hash no selo `%s`)' % (rname, ' — resultado PARCIAL' if partial else '', r64[:16], V['qp_selo16']))
    else:
        V['qp_arq_txt'] = 'AUSENTE no Nós' if hd is None else 'sha16 `%s` (= o hash no selo `%s`)' % (str(hd)[:16], V['qp_selo16'])
    # details e cpuref, em prosa (amarrados por sha256, ou o motivo dito)
    _neg_txt = ' '.join(NEG_EXTRA)
    V['qp_det_txt'] = ('`%s`' % V['qp_det16']) if qp.get('details_sha256') else ('não amarrado' if '`details.jsonl` não está amarrado' in _neg_txt else 'AUSENTE')
    V['qp_cpu_txt'] = ('`%s`' % V['qp_cpu16']) if qp.get('cpuref_sha256') else ('não amarrado' if '`cpuref.json` não está amarrado' in _neg_txt else 'AUSENTE')
    V['qp_custodia_txt'] = ('o arquivo do pilar no Nós: %s; resultado registrado `%s`; details %s; cpuref %s; pasta da rodada: %s; marca da rodada `%s`'
                            % (V['qp_arq_txt'], V['qp_res16'], V['qp_det_txt'], V['qp_cpu_txt'], V['qp_pasta_txt'], V['qp_run_id8']))
    # o cache (a ferramenta de reaproveitamento)
    ru = qp.get('reuse') or {}
    if ru.get('saved_to_cache'):
        _cr = os.path.join(ru['saved_to_cache'], 'result.json')
        _ok = os.path.exists(_cr) and sha(_cr) == qp.get('result_sha256')
        V['qp_cache'] = ('gravado no cache para reaproveitamento pela chave (%s)' % ('o sha256 confere' if _ok else 'o sha256 NAO confere'))
        if not _ok:
            P.append('o cache do pilar nao confere com o resultado')
    elif ru.get('not_cached_code'):
        V['qp_cache'] = 'não foi ao cache: `%s` (%s)' % (ru.get('not_cached_code'), ru.get('not_cached_because'))
    elif ru.get('reused'):
        V['qp_cache'] = 'REAPROVEITADO do cache (rodada intermediária)'
        P.append('o pilar foi REAPROVEITADO: a versao final roda completa')
    else:
        V['qp_cache'] = 'não foi ao cache (%s)' % (ru.get('cache_error') or 'o registro não traz o passo do cache: o pilar não chegou a ter resultado lido')
    try:
        _t0 = time.mktime(time.strptime(str(qp.get('started'))[:19], '%Y-%m-%d %H:%M:%S')); _t1 = time.mktime(time.strptime(str(qp.get('finished'))[:19], '%Y-%m-%d %H:%M:%S'))
        V['qp_min'] = '%.0f' % ((_t1 - _t0) / 60.0)
    except (ValueError, TypeError):
        V['qp_min'] = 'n/d'
    # os NUMEROS (lidos do resumo do registro, que a propria _qp_summary do rito montou do resultado). SEM resumo: n/d, dito -- nada e' recalculado aqui
    # (a leitura nao executa codigo do um.py nem do pacote; 7o achado da revisao de 04/10)
    S = qp.get('summary') or {}
    V['resumo_ausente'] = not S
    V['resumo_fonte'] = 'o registro do core (a _qp_summary do rito)' if S else ('AUSENTE no registro do core (%s): os números ficam n/d; nada recalculado' % (qp.get('summary_error') or 'sem resultado lido'))
    t2 = S.get('T2') or {}; t1 = S.get('T1') or {}; t3 = S.get('T3') or {}; t4 = S.get('T4') or {}; dd = S.get('D128') or {}; cpu = S.get('cpuref') or {}
    V['t2_configs'] = t2.get('configs', 'n/d'); V['t2_points'] = t2.get('points', 'n/d'); V['t2_unique'] = t2.get('unique', 'n/d'); V['t2_amb'] = t2.get('ambiguous', 'n/d')
    V['t2_deg'] = t2.get('degenerate', 'n/d'); V['t2_err'] = t2.get('errors', 'n/d'); V['t2_name'] = t2.get('name_in_core_configs', 'n/d'); V['t2_folds'] = t2.get('folds_window_configs', 'n/d')
    V['t2_gapmin'] = _e(t2.get('gap_rel_min')); V['t2_sin2'] = _e((t2.get('identities') or {}).get('sin2_thetaM_minus_beta'))
    _ic = t2.get('identities_checked') or {}
    V['t2_ids'] = ', '.join('%s %s' % (k, v) for k, v in _ic.items()) or 'n/d'
    V['t1_inj'] = t1.get('injections', 'n/d'); V['t1_err'] = t1.get('errors', 'n/d')
    _pd = t1.get('per_d') or {}
    V['t1_rec'] = '%d de %d dimensões' % (sum(1 for v in _pd.values() if v.get('pass_sigma0') == 1.0), len(_pd)) if _pd else 'n/d'
    V['t1_por_d'] = '; '.join('d = %s: %s injeções, sem ruído %s' % (d, v.get('n'), _pct(v.get('pass_sigma0'))) for d, v in sorted(_pd.items(), key=lambda x: int(x[0]))) or 'n/d'
    # T1 COM RUIDO: a estatistica que o V1 fixou para RELATAR (testes.T1.criterio): a fracao com beta e p dentro do criterio da especificacao, com o ramo
    # certificado, por d -- lida do resultado (o resumo do rito nao a leva); sem limiar de decisao (curva de resolucao)
    _RT1 = R.get('T1') if (isinstance(R.get('T1'), dict) and not R['T1'].get('error')) else {}
    _partes = []
    for sg in sorted((k for k in _crit_t1 if float(k) > 0), key=float):
        c_ = _crit_t1[sg]; it = []
        for d, v in sorted(_RT1.items(), key=lambda x: int(x[0])):
            lv = (v or {}).get('sigma_' + repr(float(sg))) or {}
            if lv.get('n'):
                it.append('d = %s: %s de %d' % (d, _pct(lv.get('pass_frac')), lv['n']))
        if it:
            _partes.append('σ = %s: %s' % (sg, ', '.join(it)))
    _c1 = next((_crit_t1[k] for k in sorted(_crit_t1, key=float) if float(k) > 0), {})
    V['t1_ruido_crit'] = 'β dentro de %s (relativo) e p dentro de %s (absoluto), com o ramo certificado' % (_pct(_c1.get('beta_rel')), _num(_c1.get('p_abs')))
    V['t1_ruido'] = '; '.join(_partes) or 'n/d'
    _ctl = t3.get('controls') or {}
    V['t3_ctl'] = '%d de %d' % (sum(1 for d in _ctl.values() for b in d.values() if b), sum(len(d) for d in _ctl.values())) if _ctl else 'n/d'
    _n1 = [bool((d or {}).get('N1_dephasing_only')) for d in _ctl.values()]
    V['t3_n1'] = '%d de %d dimensões' % (sum(_n1), len(_n1)) if _n1 else 'n/d'
    _n2 = t3.get('N2_unital_identity') or {}
    V['t3_n2'] = '%d de %d dimensões' % (sum(1 for d in _n2.values() if d.get('identity_ok')), len(_n2)) if _n2 else 'n/d'
    _n3 = t3.get('N3_linear_law') or {}
    V['t3_n3'] = '; '.join('d = %s: lei linear recuperada %s, lei-raiz rejeitada %s' % (d, _pct(v.get('p_recovered_sigma0')), _pct(v.get('root_law_rejected'))) for d, v in sorted(_n3.items(), key=lambda x: int(x[0]))) or 'n/d'
    for k, kk in (('t4_n', 'instances'), ('t4_u', 'unique'), ('t4_amb', 'ambiguous'), ('t4_deg', 'degenerate'), ('t4_err', 'errors'), ('t4_viol', 'identity_violations'), ('t4_rot', 'rotated'), ('t4_all', 'all_identities_checked')):
        V[k] = t4.get(kk, 'n/d')
    V['d128_code'] = str(dd.get('status_code') or 'NOT_RUN')   # o mesmo padrao da arvore (derive_verdict)
    if dd.get('ran'):
        V['d128_txt'] = 'rodou: atrator %s (n0 = %s; modo zero %s; CCI %s; espectro em %s s)' % (dd.get('status'), dd.get('n0'), 'conferido' if dd.get('zero_mode_ok') else 'NÃO conferido', _f(dd.get('cci'), 4), _f(dd.get('spectrum_s'), 0))
    else:
        V['d128_txt'] = 'não rodou nesta rodada (`%s`)' % V['d128_code']
    V['cpu_read'] = cpu.get('read', 'n/d'); V['cpu_cmp'] = cpu.get('compared', 'n/d'); V['cpu_near'] = cpu.get('near_threshold_not_compared', 'n/d'); V['cpu_dis'] = cpu.get('disagreements', 'n/d')
    _md = {k: v for k, v in (cpu.get('max_diffs') or {}).items() if k not in (cpu.get('informative_only') or []) and isinstance(v, (int, float))}
    V['cpu_maxdiff'] = ('%s (%s)' % (_e(max(_md.values())), max(_md, key=_md.get))) if _md else 'n/d'
    _eng = S.get('engine') or []
    V['eng'] = '%d de %d' % (sum(1 for c in _eng if c.get('ok')), len(_eng)) if _eng else 'n/d'
    _ps = S.get('phase_seconds') or {}
    V['fases'] = ', '.join('%s %.0f min' % (k, v / 60.0) for k, v in _ps.items() if isinstance(v, (int, float))) or 'n/d'
    _env = S.get('env') or {}
    V['qp_gpu'] = '%s; PyTorch %s; CUDA %s' % (_env.get('gpu'), _env.get('torch'), _env.get('cuda')) if _env else 'n/d'
    # a CLASSE, com a causa em prosa (tirada do token do veredito)
    V['qp_causa'] = causa_do_veredito(V['qp_v'], V['qp_classe'], R, qp)
    V['qp_classe_base'] = CLASSE_TXT[V['qp_classe']]
    V['qp_classe_txt'] = V['qp_classe_base'] + ((' — causa: ' + V['qp_causa']) if V['qp_causa'] else '')
    # os NEGATIVOS, em dois grupos: (a) os da LISTA do pre-registro (resultados_negativos_honestos do V1); (b) os ditos pela gerencia, AO LADO (fora da lista)
    NEG_PRE = []; NEG_GER = []
    if V['qp_classe'] == 'RAMO_9':
        tk = tokens_ramo9(V['qp_v'])
        if S:
            _u = (t2.get('unique'), t2.get('points'))
            if tk['attr'] != _u:
                P.append('o token ATTRACTOR_UNIQUE (%s) != o resumo do T2 (%s)' % (tk['attr'], _u))
            if tk['stress'] != (t4.get('instances'), t4.get('unique'), t4.get('all_identities_checked')):
                P.append('o token STRESS (%s) != o resumo do T4' % (tk['stress'],))
            if tk['name'] != (t2.get('name_in_core_configs'), t2.get('configs')) or tk['folds'] != (t2.get('folds_window_configs'), t2.get('configs')):
                P.append('os tokens NAME_IN_CORE/FOLDS_WINDOW (%s/%s) != o resumo do T2' % (tk['name'], tk['folds']))
            _rec = bool(_pd) and all(v.get('pass_sigma0') == 1.0 for v in _pd.values())
            if tk['t1'] != ('RECOVERS_INJECTED_LAW_BLIND' if _rec else 'DOES_NOT_RECOVER_INJECTED_LAW'):
                P.append('o token do T1 (%s) != o resumo do T1' % tk['t1'])
            _d = ('D128_' + str(dd.get('status', 'NA'))) if dd.get('ran') else ('D128_INTERRUPTED' if V['d128_code'] == 'STARTED' else 'D128_' + V['d128_code'])
            if tk['d128'] != _d:
                P.append('o token do D128 (%s) != o resumo (%s)' % (tk['d128'], _d))
        else:
            NEG_EXTRA.append('os números do pilar não vieram no registro do core (resumo %s): o texto diz o veredito da árvore e n/d' % V['resumo_fonte'])
        if not (tk['ctl'] and tk['ids'] and tk['cpu']):
            P.append('o ramo 9 sem CONTROLS_FAILED_AS_REQUIRED/IDENTITIES_HOLD/CPU_REFERENCE_AGREES')
        if tk['attr'] and tk['attr'][0] < tk['attr'][1]:
            NEG_PRE.append('o atrator não é único em %d de %d pontos da grade' % (tk['attr'][1] - tk['attr'][0], tk['attr'][1]))
        if tk['t1'] == 'DOES_NOT_RECOVER_INJECTED_LAW':
            NEG_PRE.append('o instrumento NÃO recupera a lei injetada sem ruído em todas as dimensões (T1)')
        if tk['name'] and tk['name'][0] < tk['name'][1]:
            NEG_PRE.append('NAME_IN_CORE em %d de %d configurações (em %d, nenhum ponto de atrator único guarda metade do peso no núcleo)' % (tk['name'][0], tk['name'][1], tk['name'][1] - tk['name'][0]))
        if tk['folds'] and tk['folds'][0] == 0 and tk['folds'][1] > 0:
            NEG_PRE.append('FOLDS_WINDOW em 0 de %d configurações (a janela das dobras, quase-pureza do atrator, não aparece com γ livre em nenhuma)' % tk['folds'][1])
        elif tk['folds'] and tk['folds'][0] < tk['folds'][1]:
            NEG_GER.append('FOLDS_WINDOW em %d de %d configurações (a janela das dobras, quase-pureza do atrator, não aparece com γ livre em %d)' % (tk['folds'][0], tk['folds'][1], tk['folds'][1] - tk['folds'][0]))
        if tk['stress'] and tk['stress'][1] < tk['stress'][0]:
            NEG_PRE.append('no estresse (T4), atrator não único em %d de %d instâncias' % (tk['stress'][0] - tk['stress'][1], tk['stress'][0]))
        if tk['d128'] and tk['d128'] != 'D128_UNIQUE' and (tk['d128'].startswith('D128_NOT_RUN') or tk['d128'] == 'D128_INTERRUPTED'):
            NEG_PRE.append('o D128 não rodou (`%s`): a escala d = 128 não foi alcançada nesta rodada' % tk['d128'])
        elif tk['d128'] and tk['d128'] != 'D128_UNIQUE':
            NEG_GER.append('o D128 rodou e, em d = 128, o atrator é `%s`' % tk['d128'][5:])
        if V['qp_all_verified'] is not True:
            P.append('ramo 9 com all_verified != True')
        if 'quantum_pillar_v384' in V['balde_l']:
            P.append('ramo 9 no terceiro balde do selo')
    else:
        if V['qp_all_verified'] is True:
            P.append('pilar nao concluido com all_verified True')
        if 'quantum_pillar_v384' not in V['balde_l']:
            P.append('o pilar nao concluido nao esta no terceiro balde do selo (computacao_nao_concluida)')
    NEG_GER += NEG_EXTRA
    V['qp_neg_prereg_l'] = NEG_PRE; V['qp_neg_ger_l'] = NEG_GER; V['qp_neg_extra_l'] = NEG_EXTRA
    V['qp_neg_extra'] = '; '.join(NEG_EXTRA)
    if V['qp_classe'] == 'RAMO_9':
        V['qp_negativos_l'] = NEG_PRE + NEG_GER
        V['qp_negativos'] = (('da lista do pré-registro: ' + ('; '.join(NEG_PRE) if NEG_PRE else 'nenhum'))
                             + (('; ditos pela gerência, ao lado (fora da lista do V1): ' + '; '.join(NEG_GER)) if NEG_GER else ''))
    else:
        V['qp_negativos_l'] = [V['qp_classe_txt']] + NEG_GER
        V['qp_negativos'] = V['qp_classe_txt'] + (('; ditos pela gerência, ao lado: ' + '; '.join(NEG_GER)) if NEG_GER else '')
    # a guarda de palavra proibida em TODOS os vereditos do core (a MESMA do rito)
    proib = [k for k, mm in core.items() if isinstance(mm, dict) and (GUARDA.search(str(mm.get('verdict') or '')) or 'TGL_PROVED' in str(mm.get('verdict') or '') or 'CONSCIOUSNESS_PROVED' in str(mm.get('verdict') or ''))]
    if proib:
        P.append('veredito proibido: %s' % proib)
    # a custodia da v383 (lida do git da Central: os commits de custodia levam «custodia(vNNN)»; SO LEITURA) e o marcador do servidor (informacao)
    V['v383_commit'] = ''
    try:
        import subprocess
        _g = subprocess.run(['git', '-C', os.path.dirname(A.ATLAS_DIR_REAL), 'log', '--oneline', '-400'], capture_output=True, text=True, encoding='utf-8', timeout=60)
        _c = [l for l in _g.stdout.splitlines() if 'custodia(v383)' in l]
        V['v383_commit'] = _c[0][:80] if _c else ''
        V['v383_git_lido'] = _g.returncode == 0
    except Exception as e_:
        V['v383_git_lido'] = False
    if not V.get('v383_git_lido'):
        P.append('o git da Central nao foi lido (a custodia da v383 nao pode ser dita)')
    _mk = os.path.join(PK, '.servidor_parado_pelo_rito')
    V['marcador_txt'] = ('PRESENTE (%s) — conferir a tarefa «IALD Llama Server»' % open(_mk, encoding='utf-8', errors='replace').read().strip()) if os.path.exists(_mk) else 'ausente (o lançador o remove quando o servidor volta)'
    try:
        V['data'] = time.strftime('%d/%m/%Y', time.strptime(V['selo_ts'][:10], '%Y-%m-%d'))
    except ValueError:
        V['data'] = time.strftime('%d/%m/%Y')
    return V, P


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    V, P = ler()
    print(json.dumps({k: v for k, v in V.items() if k not in ('qp_reading',)}, ensure_ascii=False, indent=1, default=str))
    print('PROBLEMAS:', P if P else 'nenhum')
    sys.exit(2 if P else 0)
