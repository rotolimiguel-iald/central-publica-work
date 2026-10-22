# -*- coding: utf-8 -*-
"""SO PARA O ENSAIO (corretor, 04/10): transforma uma COPIA do Nos SINTETICO (com a marca SINTETICO_ENSAIO_V384.txt) num Nos SINTETICO COERENTE em que o
pilar caiu numa CLASSE da arvore -- imitando, passo a passo, o que o trabalhador (pilar_quantico_worker.py: main/derive_verdict/write_result) e o runtime
(v384_runtime.py: quantum_pillar_start_v384 / quantum_pillar_finish_v384 / _qp_out_marker) gravariam: o arquivo de resultado (result.json com .sha256, ou
result_partial.json sem ele), os arquivos amarrados ou nao, o registro do core, o do selo (as chaves W07), o arquivo do pilar no Nos (o resultado, o parcial
ou o MARCADOR), o terceiro balde e as linhas [v384] do stdout. O veredito de cada classe segue a forma da arvore congelada (sem importar nem rodar o
trabalhador); o resumo e' o da _qp_summary do PACOTE (v384_runtime.py), conferida igual a do candidato por texto -- nunca a do um.py do Nos.
NUNCA escreve fora da pasta-alvo (que tem de estar dentro de v384_selo e ter a marca); arquivos grandes ligados por hardlink sao REMOVIDOS antes de reescritos.
Classes: PARCIAL_PRAZO_T4, PARCIAL_D128, ANULADO_CPU_AUSENTE, ANULADO_CONTROLE, NAO_RODOU_FATAL, MOTOR_FALHOU, NAO_RODOU_SEM_ARQUIVO,
NAO_RODOU_RECUSA_UMPY, FASE_FALHOU_T2, RAMO9_NEGATIVOS (o ramo 9 com negativos: o conferidor congelado o aprova).
uso como biblioteca: transforma(N, nome); uso direto: python variantes_pilar_v384.py <pasta_destino> <classe> (copia o Nos sintetico do ensaio e transforma)."""
import hashlib, json, os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ambiente_v384 as A
PRE = 'TGL_QUANTUM_PILLAR_V1__'
CLASSES = ('PARCIAL_PRAZO_T4', 'PARCIAL_D128', 'ANULADO_CPU_AUSENTE', 'ANULADO_CONTROLE', 'NAO_RODOU_FATAL', 'MOTOR_FALHOU', 'NAO_RODOU_SEM_ARQUIVO',
           'NAO_RODOU_RECUSA_UMPY', 'FASE_FALHOU_T2', 'RAMO9_NEGATIVOS')
CLASSE_ESPERADA = {'PARCIAL_PRAZO_T4': 'PARCIAL', 'PARCIAL_D128': 'PARCIAL', 'ANULADO_CPU_AUSENTE': 'ANULADO', 'ANULADO_CONTROLE': 'ANULADO',
                   'NAO_RODOU_FATAL': 'NAO_RODOU', 'MOTOR_FALHOU': 'MOTOR_FALHOU', 'NAO_RODOU_SEM_ARQUIVO': 'NAO_RODOU', 'NAO_RODOU_RECUSA_UMPY': 'NAO_RODOU',
                   'FASE_FALHOU_T2': 'FASE_FALHOU', 'RAMO9_NEGATIVOS': 'RAMO_9'}
sha = lambda b: hashlib.sha256(b).hexdigest()
_QS = None


def _fatia(t, nome):
    i = t.index('\ndef %s(' % nome) + 1; j = t.index('\ndef ', i + 1)
    return t[i:j].rstrip() + '\n'


def qp_summary():
    """A _qp_summary do PACOTE (v384_runtime.py), conferida igual a do candidato (um_v384_candidato.py, sha16 = CANDIDATO) por texto. So para o ensaio."""
    global _QS
    if _QS is None:
        CM = json.load(open(os.path.join(A.PK, 'CANDIDATO_v384.json'), encoding='utf-8'))
        cb = open(os.path.join(A.PK, 'um_v384_candidato.py'), 'rb').read(); assert sha(cb)[:16] == CM['sha16']
        rt = open(os.path.join(A.PK, 'v384_runtime.py'), encoding='utf-8').read()
        s = _fatia(rt, '_qp_summary'); assert s == _fatia(cb.decode('utf-8').replace('\r\n', '\n'), '_qp_summary'), 'a _qp_summary do pacote != a do candidato'
        ns = {}; exec(compile(s, '<_qp_summary do pacote v384_runtime.py>', 'exec'), ns); _QS = ns['_qp_summary']
    return _QS


def _guarda(N):
    assert os.path.exists(os.path.join(N, A.MARCA_SINT)), 'so num Nos SINTETICO'
    assert os.path.realpath(N).lower().startswith(os.path.realpath(A.SEL).lower() + os.sep), 'so dentro de v384_selo'
    assert os.path.normcase(os.path.realpath(N)) != os.path.normcase(os.path.realpath(A.NOS_REAL))


def _w(p, b):
    if os.path.exists(p):
        os.remove(p)          # quebra o hardlink: nunca escrever atraves dele
    with open(p + '.tmp', 'wb') as f:
        f.write(b)
    assert os.path.getsize(p + '.tmp') == len(b); os.replace(p + '.tmp', p)


def _rm(p):
    if os.path.exists(p):
        os.remove(p)


def _write_result(rd, nome, R):
    b = json.dumps(R, ensure_ascii=False, indent=1).encode('utf-8'); h = sha(b)
    _w(os.path.join(rd, nome), b)
    if nome == 'result.json':
        _w(os.path.join(rd, 'result.json.sha256'), h.encode('ascii'))
    return b, h


def _marcador(verdict, reason, absent, run_id, key):
    return json.dumps({'verdict': verdict, 'marker': True, 'reason': reason, 'result_file_absent': absent, 'run_id': run_id, 'key': key}, ensure_ascii=False, indent=1).encode('utf-8')


def transforma(N, nome):
    _guarda(N)
    assert nome in CLASSES, nome
    cp = os.path.join(N, 'um_absoluto.json'); spp = os.path.join(N, 'um_absoluto_selo.json'); stp = os.path.join(N, 'rodada_v384_stdout.txt')
    RES = json.load(open(cp, encoding='utf-8')); S = json.load(open(spp, encoding='utf-8'))
    qp0 = RES['core']['quantum_pillar_v384']
    rd = qp0['run_dir']; assert os.path.normcase(os.path.realpath(rd)).startswith(os.path.normcase(os.path.realpath(N)) + os.sep), ('o run_dir do core nao esta no Nos de teste', rd)
    R0 = json.load(open(os.path.join(rd, 'result.json'), encoding='utf-8'))
    v0 = qp0['verdict']
    keep = {k: qp0[k] for k in ('theorem', 'status', 'preregistration', 'key', 'beta_hex', 'checkpoint_switch', 'mode', 'does_not_gate_core') if k in qp0}
    reuse_nc = {'reused': False, 'reading': 'PILAR_QUANTICO_CALCULADO_NESTA_RODADA [SINTETICO]', 'not_cached_code': 'NOT_COMPLETE_OR_NOT_CHECKED',
                'not_cached_because': 'resultado nao completo ou nao conferido'}
    launch, finish_line = True, True
    nos_bytes = None

    def com_resultado(R, verdict, nome_arq='result.json', **extra):
        """o registro como o runtime o monta DEPOIS de ler um arquivo de resultado (e copiar ao Nos)."""
        b, h = _write_result(rd, nome_arq, R)
        q = dict(keep, worker_rc=extra.pop('worker_rc', 0), timed_out=extra.pop('timed_out', False), result_sha256=h, result_sha_file_ok=(nome_arq == 'result.json'),
                 partial=(nome_arq != 'result.json'), worker_sha256=R.get('worker_sha256'), run_id=R.get('run_id'), spec_sha256_in_result=R.get('spec_sha256'),
                 details_sha256=R.get('details_sha256'), cpuref_sha256=R.get('cpuref_sha256'), run_dir=rd, verdict_worker=R.get('verdict'),
                 verdict_rederived=extra.pop('der'), started=R.get('started'), finished=R.get('finished'), beta_matches_core=True, verdict=verdict,
                 custody_chain_ok=extra.pop('custody'), all_verified=extra.pop('all_verified', False), summary=qp_summary()(R), out_file_sha256=h, copied_to_out=True,
                 reuse=extra.pop('reuse', reuse_nc), SINTETICO_ENSAIO_V384=qp0.get('SINTETICO_ENSAIO_V384'))
        assert not extra, extra
        return q, b
    if nome == 'PARCIAL_PRAZO_T4':
        R = {k: v for k, v in R0.items() if k not in ('T4', 'details_sha256', 'cpuref_sha256', 'cpuref_compare', 'D128', 'finished', 'verdict')}
        R['phase_seconds'] = {k: v for k, v in (R0.get('phase_seconds') or {}).items() if k in ('T3', 'T2', 'T1')}
        _rm(os.path.join(rd, 'result.json')); _rm(os.path.join(rd, 'result.json.sha256'))
        der = PRE + 'PHASE_T4_FAILED__RESULTS_INCOMPLETE__GATE_UNTOUCHED'
        verdict = der.replace('__GATE_UNTOUCHED', '__PARTIAL_RESULT_WORKER_STOPPED_BY_TIMEOUT__GATE_UNTOUCHED')
        qp, nos_bytes = com_resultado(R, verdict, 'result_partial.json', der=der, custody=False, worker_rc=None, timed_out=True)
    elif nome == 'PARCIAL_D128':
        R = {k: v for k, v in R0.items() if k not in ('finished', 'verdict')}
        R['D128'] = {'started': True, 'ran': False, 'status_code': 'STARTED'}
        _rm(os.path.join(rd, 'result.json')); _rm(os.path.join(rd, 'result.json.sha256'))
        der = v0.replace('__SINTETICO_FUMACA_NAO_E_RESULTADO', '').replace('D128_NOT_RUN_DEADLINE', 'D128_INTERRUPTED')
        assert der != v0 and '__D128_INTERRUPTED__' in der
        verdict = der.replace('__GATE_UNTOUCHED', '__PARTIAL_RESULT_WORKER_STOPPED_BY_TIMEOUT__GATE_UNTOUCHED')
        qp, nos_bytes = com_resultado(R, verdict, 'result_partial.json', der=der, custody=False, worker_rc=None, timed_out=True)
    elif nome == 'ANULADO_CPU_AUSENTE':
        R = dict(R0); R.pop('cpuref_sha256', None)
        R['cpuref_compare'] = {'ok': False, 'error': 'cpuref.json ausente', 'error_code': 'CPUREF_JSON_ABSENT', 'child_rc': None}
        for f in ('cpuref.json', 'cpuref.json.sha256'):
            _rm(os.path.join(rd, f))
        verdict = R['verdict'] = PRE + 'CPU_REFERENCE_DISAGREES_OR_ABSENT__RESULTS_VOID__GATE_UNTOUCHED'
        qp, nos_bytes = com_resultado(R, verdict, der=verdict, custody=True)
    elif nome == 'ANULADO_CONTROLE':
        R = json.loads(json.dumps(R0))
        dks = sorted(k for k in R['T3'] if k.startswith('d'))
        R['T3'][dks[-1]]['N1_dephasing_only']['failed_as_required'] = False; R['T3'][dks[-1]]['N1_dephasing_only']['status'] = 'UNIQUE'
        verdict = R['verdict'] = PRE + 'CONTROL_DID_NOT_FAIL__INSTRUMENT_BLIND__RESULTS_VOID__GATE_UNTOUCHED'
        qp, nos_bytes = com_resultado(R, verdict, der=verdict, custody=True)
    elif nome == 'NAO_RODOU_FATAL':
        R = {k: v for k, v in R0.items() if k not in ('details_sha256', 'cpuref_sha256', 'cpuref_compare', 'D128', 'T4', 'finished')}
        R['fatal'] = "RuntimeError('CUDA error: out of memory') [SINTETICO]"; R['trace'] = 'Traceback (most recent call last): ... [SINTETICO]'; R['parent_gone'] = False
        for f in ('cpuref.json', 'cpuref.json.sha256'):
            _rm(os.path.join(rd, f))
        verdict = R['verdict'] = PRE + 'NOT_RUN__WORKER_FATAL__GATE_UNTOUCHED'
        qp, nos_bytes = com_resultado(R, verdict, der=verdict, custody=True, worker_rc=1)
    elif nome == 'MOTOR_FALHOU':
        R = {k: R0[k] for k in ('worker', 'mode', 'run_id', 'started', 'worker_sha256', 'status_statement', 'spec_sha256', 'beta_hex', 'beta', 'env') if k in R0}
        es = json.loads(json.dumps(R0.get('engine_selftest') or {})); es['all_ok'] = False
        if es.get('checks'):
            es['checks'][1]['ok'] = False
        R['engine_selftest'] = es
        for f in ('details.jsonl', 'cpuref.json', 'cpuref.json.sha256', 'progress.json'):
            _rm(os.path.join(rd, f))
        verdict = R['verdict'] = PRE + 'ENGINE_SELFTEST_FAILED__NO_RESULT__GATE_UNTOUCHED'
        qp, nos_bytes = com_resultado(R, verdict, der=verdict, custody=True, worker_rc=5)
    elif nome == 'FASE_FALHOU_T2':
        R = json.loads(json.dumps(R0)); R['T2'] = {'error': "ValueError('a fase T2 caiu') [SINTETICO]", 'trace': '... [SINTETICO]'}
        verdict = R['verdict'] = PRE + 'PHASE_T2_FAILED__RESULTS_INCOMPLETE__GATE_UNTOUCHED'
        qp, nos_bytes = com_resultado(R, verdict, der=verdict, custody=True)
    elif nome == 'RAMO9_NEGATIVOS':
        R = json.loads(json.dumps(R0))
        cf = R['T2']['configs']
        for c in cf[:2]:                       # o atrator nao unico em 2 pontos
            c['unique'] -= 1; c['ambiguous'] += 1
        for c in cf:                           # FOLDS_WINDOW 0 de n (da lista do V1)
            c['folds_window'] = False
        cf[-1]['cci_half_window'] = None       # NAME_IN_CORE n-1 de n
        d4 = sorted(R['T4'])[0]; R['T4'][d4]['UNIQUE'] -= 1; R['T4'][d4]['AMBIGUOUS'] += 1
        npts = sum(c['n_points'] for c in cf); nun = sum(c['unique'] for c in cf); nconf = len(cf); nm = sum(1 for c in cf if c['cci_half_window'])
        n4 = sum(a['n'] for a in R['T4'].values()); u4 = sum(a['UNIQUE'] for a in R['T4'].values()); m4 = sum(a['all_identities_checked'] for a in R['T4'].values())
        verdict = (PRE + 'FIVE_JUMP_GKLS__ATTRACTOR_UNIQUE_%d_OF_%d_ON_THE_GRID__T1_INSTRUMENT_RECOVERS_INJECTED_LAW_BLIND__CONTROLS_FAILED_AS_REQUIRED__IDENTITIES_HOLD__'
                   'STRESS_%d_INSTANCES_%d_UNIQUE_ALL_IDENTITIES_CHECKED_IN_%d__NAME_IN_CORE_%d_OF_%d_ON_THE_GRID__FOLDS_WINDOW_0_OF_%d_ON_THE_GRID__D128_NOT_RUN_DEADLINE__'
                   'CPU_REFERENCE_AGREES__COMPUTED_NOT_MEASURED__SINTETICO_VARIANTE_NAO_E_RESULTADO__GATE_UNTOUCHED' % (nun, npts, n4, u4, m4, nm, nconf, nconf))
        R['verdict'] = verdict
        rq = dict(qp0['reuse'])
        qp, nos_bytes = com_resultado(R, verdict, der=verdict, custody=True, all_verified=True, reuse=rq)
    elif nome == 'NAO_RODOU_SEM_ARQUIVO':
        # o trabalhador foi lancado e morreu antes do 1o parcial: o runtime volta antes do update com o run_dir; o MARCADOR desta rodada vai ao Nos
        for f in os.listdir(rd):
            _rm(os.path.join(rd, f))
        _w(os.path.join(rd, 'worker_stdout.txt'), b'[SINTETICO] o trabalhador morreu antes do primeiro parcial (CUDA error: device-side assert) [SINTETICO]\n')
        rid = str(R0['run_id']).replace('SINTETICO_', '')     # a marca da rodada que nomeia a pasta (run_<ts>_<run8>)
        verdict = PRE + 'NOT_RUN__NO_RESULT_FILE__GATE_UNTOUCHED'
        nos_bytes = _marcador(verdict, 'no_result_file', True, rid, keep.get('key'))
        qp = dict(keep, worker_rc=1, timed_out=False, verdict=verdict, all_verified=False, out_file_sha256=sha(nos_bytes),
                  preregistration=dict(keep['preregistration']), SINTETICO_ENSAIO_V384=qp0.get('SINTETICO_ENSAIO_V384'))
        finish_line = False
    elif nome == 'NAO_RODOU_RECUSA_UMPY':
        # o um.py recusou ANTES do Popen (a especificacao embutida sem o hash congelado): sem pasta da rodada, sem a linha de lancamento, sem a linha do veredito
        shutil.rmtree(rd)
        verdict = PRE + 'NOT_RUN__SPEC_HASH_MISMATCH_IN_UM_PY__GATE_UNTOUCHED'
        nos_bytes = _marcador(verdict, 'not_run', None, None, None)
        pr = {k: v for k, v in keep['preregistration'].items() if k != 'on_disk_matches'}
        qp = {'theorem': keep['theorem'], 'status': keep['status'], 'preregistration': pr, 'key': None, 'beta_hex': None, 'checkpoint_switch': False, 'mode': None,
              'does_not_gate_core': True, 'verdict': verdict, 'all_verified': False, 'refused': 'SPEC_HASH_MISMATCH_IN_UM_PY', 'out_file_sha256': sha(nos_bytes),
              'SINTETICO_ENSAIO_V384': qp0.get('SINTETICO_ENSAIO_V384')}
        launch, finish_line = False, False
    _w(os.path.join(N, 'um_absoluto_pilar_quantico.json'), nos_bytes)
    RES['core']['quantum_pillar_v384'] = qp
    _w(cp, json.dumps(RES, ensure_ascii=False, indent=1).encode('utf-8'))
    S['quantum_pillar_v384'] = {k: qp.get(k) for k in S['quantum_pillar_v384']}
    S['sha256']['um_absoluto_pilar_quantico.json'] = sha(nos_bytes)
    S['not_sealed_this_run']['computacao_nao_concluida'] = [] if verdict.startswith(PRE + 'FIVE_JUMP_GKLS__') and '__PARTIAL_RESULT_' not in verdict else ['quantum_pillar_v384']
    S['SINTETICO_VARIANTE_V384'] = nome
    _w(spp, json.dumps(S, ensure_ascii=False, indent=2).encode('utf-8'))
    balde = ', '.join(S['not_sealed_this_run']['computacao_nao_concluida']) or 'nenhuma'
    out = []
    for l in open(stp, encoding='utf-8').read().split('\n'):
        if l.startswith('[v384] pilar quantico: o trabalhador da GPU foi lancado') and not launch:
            continue
        if l.startswith('[v384] pilar quantico: TGL_QUANTUM_PILLAR'):
            if not finish_line:
                continue
            l = '[v384] pilar quantico: ' + verdict
        if l.startswith('   [v384] o pilar quantico ('):
            l = l.split('): ', 1)[0] + '): ' + verdict
        if l.startswith('[selo] custodia de sentido: '):
            l = l.split(' | computacao nao concluida: ')[0] + ' | computacao nao concluida: ' + balde
        out.append(l)
    _w(stp, '\n'.join(out).encode('utf-8'))
    return verdict


def copia_nos(dst, origem=None):
    """copia o Nos sintetico do ensaio para dst (hardlink nos arquivos > 1 MB que a variante nao reescreve: o um.py) e reaponta o run_dir do core/selo."""
    origem = origem or os.path.join(A.SEL, 'ensaio_nos_sintetico')
    assert os.path.exists(os.path.join(origem, A.MARCA_SINT))
    assert os.path.realpath(dst).lower().startswith(os.path.realpath(A.SEL).lower() + os.sep)
    if os.path.isdir(dst):
        assert os.path.exists(os.path.join(dst, A.MARCA_SINT)), 'o destino existe e NAO e sintetico -- nao apago'
        shutil.rmtree(dst)
    for root, _ds, fs in os.walk(origem):
        for f in fs:
            s = os.path.join(root, f); q = os.path.join(dst, os.path.relpath(s, origem)); os.makedirs(os.path.dirname(q), exist_ok=True)
            os.link(s, q) if (os.path.getsize(s) > 1 << 20 and f == 'um.py') else shutil.copy2(s, q)
    for nm in ('um_absoluto.json', 'um_absoluto_selo.json'):
        p = os.path.join(dst, nm); b = open(p, encoding='utf-8').read().replace(json.dumps(origem)[1:-1], json.dumps(dst)[1:-1])
        _w(p, b.encode('utf-8'))
    return dst


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    d, c = os.path.abspath(sys.argv[1]), sys.argv[2]
    copia_nos(d); print(transforma(d, c))
