# -*- coding: utf-8 -*-
# LEITURA da rodada v380 -- SO LEITURA. Todo numero, hash e veredito sai daqui, LIDO do artefato (JSON selado, selo, stdout, kernel
# materializado, conferidor, pacote v380), nunca digitado. Usado por superficies_v380.py, manifesto_v380.py, patch_arvore_indice_v380.py, handoff_v380.py.
import os, re, json, glob, hashlib, time
HERE = os.path.dirname(os.path.abspath(__file__))
SP = os.path.dirname(HERE)
PK = os.path.join(SP, 'v380')
NOS_REAL = r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós'
FINAL_RE = re.compile(r'^\[selo\] colapso tipado: ')
TRAILER_RE = re.compile(r'^(exit=\d+|rc=\d+|RITO_RC=\d+|inicio |fim )')
NOVOS = ('bancada_fases_5_6_7_v380',)
PEDRAS = ()
LEITURAS = ('the_bancada_fases_5_6_7_reading_v380',)
PINADOS = ('physics_is_the_reading_v377', 'the_dissipation_law_v377', 'bancada_fases_v377', 'final_stone_reading_v377',
           'the_dissipation_law_with_contrast_v378', 'what_was_missed_v378', 'bancada_fase4_v378', 'the_elementary_reason_v379')
TERMO = ('gpf_H2_smooth_modular_four_frame_discharged', 'gpf_H3_local_horizon_equilibrium_discharged', 'gpi_H3_horizon_data_produced')
GUARDA = re.compile('(?<!NOT_)(?<!UN)' + 'CONF' + 'IRMED|(?<!AP)PRO' + 'VED_BY')


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def sha_txt16(p):
    return hashlib.sha256(open(p, 'r', encoding='utf-8', newline='').read().encode('utf-8')).hexdigest()[:16]


def _aplicado():
    ps = sorted(glob.glob(os.path.join(PK, 'APLICADO_AO_CANONICO_*.json')))
    assert ps, 'APLICADO_AO_CANONICO_*.json ausente no pacote v380'
    return json.load(open(ps[-1], encoding='utf-8')), ps[-1]


def _f(x, nd=2):
    return ('%.*f' % (nd, x)) if isinstance(x, (int, float)) else 'n/d'


def ler():
    P = []
    ESP = json.load(open(os.path.join(PK, 'ESPERADOS_v380.json'), encoding='utf-8'))
    ap, app = _aplicado()
    nos = os.environ.get('V380_NOS') or NOS_REAL
    V = {'nos': nos, 'aplicado_json': app}
    res = json.load(open(os.path.join(nos, 'um_absoluto.json'), encoding='utf-8'))
    selo = json.load(open(os.path.join(nos, 'um_absoluto_selo.json'), encoding='utf-8'))
    stp = os.path.join(nos, 'rodada_v380_stdout.txt')
    out = open(stp, encoding='utf-8', errors='replace').read()
    KT = os.path.join(nos, 'tgl_kernel')
    V['s16'] = sha(os.path.join(nos, 'um.py'))[:16]; V['umb'] = os.path.getsize(os.path.join(nos, 'um.py'))
    core = res['core']
    if not str((selo.get('sha256') or {}).get('um.py', '')).startswith(V['s16']):
        P.append('selo.sha256(um.py) != disco')
    V['base16'] = ap['backups']['um.py']['sha16']
    if V['base16'] != ESP['origem_sha16']:
        P.append('base lida (%s) != origem v379 de ESPERADOS (%s)' % (V['base16'], ESP['origem_sha16']))
    if ap['um_py_novo']['sha16'] != V['s16'] or ESP['candidato_sha16'] != V['s16']:
        P.append('um.py do disco (%s) != o instalado / o candidato de ESPERADOS' % V['s16'])
    m = re.search(r'teoremas limpos:\s*(\d+)/(\d+)', out)
    V['teor'] = '%s/%s' % m.groups() if m else 'AUSENTE'
    if not m or m.group(1) != m.group(2):
        P.append('teoremas limpos ausente ou N != M')
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
    mrc = re.findall(r'^(?:exit|rc|RITO_RC)=(\d+)', out, flags=re.M)
    V['rc'] = os.environ.get('V380_RC') or (mrc[-1] if mrc else 'NAO_LIDO')
    V['rcsrc'] = 'dito pela gerência (V380_RC)' if os.environ.get('V380_RC') else ('linha RITO_RC= do stdout (escrita pelo shell da gerência)' if mrc else 'ausente')
    if V['rc'] != '0':
        P.append('rc do rito nao lido como 0 (%s)' % V['rc'])
    hor = os.path.join(PK, 'rito_horarios_v380.txt')
    hh = open(hor, encoding='utf-8').read().split() if os.path.exists(hor) else []
    V['t0'] = hh[0] if hh else 'n/d'
    V['t1'] = hh[1] if len(hh) > 1 else time.strftime('%H:%M:%S', time.localtime(os.stat(stp).st_mtime))
    V['tsrc'] = 'horários gravados pelo shell da gerência' if len(hh) > 1 else 'fim = última modificação do stdout'
    V['tentativas'] = sorted(os.path.basename(p) for p in glob.glob(os.path.join(nos, 'rodada_v380_stdout_tentativa*.txt')))
    V['selo_ts'] = str(selo.get('timestamp'))
    ts_ap = '%s-%s-%s %s:%s:%s' % (ap['ts'][0:4], ap['ts'][4:6], ap['ts'][6:8], ap['ts'][9:11], ap['ts'][11:13], ap['ts'][13:15])
    if not (V['selo_ts'] >= ts_ap):
        P.append('o selo (%s) e anterior a instalacao da v380 (%s)' % (V['selo_ts'], ts_ap))
    confp = os.path.join(HERE, 'conferidor', 'conferencia_rito_v380.json'); confo = os.path.join(HERE, 'conferir_rito_v380_stdout.txt')
    try:
        C = json.load(open(confp, encoding='utf-8')); CO = open(confo, encoding='utf-8', errors='replace').read()
    except OSError as e:
        C, CO = {}, ''; P.append('conferidor nao lido: %r' % e)
    V['conf_dm'] = '%d/%d' % (sum(1 for v in (C.get('deve_mudar') or {}).values() if v), len(C.get('deve_mudar') or {}))
    V['conf_np'] = '%d/%d' % (sum(1 for v in (C.get('nao_pode_mudar') or {}).values() if v), len(C.get('nao_pode_mudar') or {}))
    V['conf16'] = sha(confp)[:16] if os.path.exists(confp) else 'AUSENTE'
    if C.get('tudo_bate') is not True or not CO.rstrip().endswith('TUDO BATE') or C.get('um_py_sha16') != V['s16']:
        P.append('conferidor NAO deu TUDO BATE para este um.py')
    novos = ESP['kernel']['new']
    V['pedras'] = {}
    _nomes = {}   # v380: sem pedra nova
    for n in PEDRAS:
        rel = 'TGLExt/%s.lean' % n; p = os.path.join(KT, *rel.split('/'))
        got = sha_txt16(p) if os.path.exists(p) else 'AUSENTE'
        V['pedras'][n] = {'sha16': got, 'n_print': len(_nomes.get(n, []))}
        if got != novos.get(rel):
            P.append('pedra %s materializada %s != esperada %s' % (n, got, novos.get(rel)))
    kf = core.get('kernel_formalization') or {}
    FL = [f for f, _ in ESP['bandeiras']]
    V['n_flags_on'] = sum(1 for f in FL if kf.get(f) is True); V['n_flags'] = len(FL)
    if V['n_flags_on'] != len(FL) or len(FL) != 0:
        P.append('bandeiras v380 acesas %d/%d' % (V['n_flags_on'], len(FL)))
    if not all(kf.get(f) is True for f in ESP['bandeiras_antigas']):
        P.append('bandeiras antigas (v377-v379) apagadas')
    V['gpc'] = {k: kf.get(k) for k in ('gpc_H2_smooth_modular_four_frame_discharged', 'gpc_H3_local_horizon_equilibrium_discharged', 'gpc_H3_horizon_data_produced')}
    if not all(v is True for v in V['gpc'].values()):
        P.append('bandeiras gpc_ nao todas True: %s' % V['gpc'])
    V['termo'] = {k: kf.get(k) for k in TERMO}
    V['hvals'] = '/'.join(str(v) for v in V['termo'].values())
    if any(v is not False for v in V['termo'].values()):
        P.append('POR TERMO nao False: %s' % V['hvals'])
    lad = core.get('external_ladder') or {}
    V['esc'] = '%s/%s' % (lad.get('n_theorems_clean'), lad.get('n_theorems_expected'))
    V['esc_ant'] = '%d/%d' % tuple(ESP['escada_v379']); V['nax'] = len(kf.get('axiom_report') or {}); V['nax_ant'] = ESP['axiom_report_v379']
    if V['esc'] != V['esc_ant']:
        P.append('a escada MUDOU numa versao sem kernel novo (%s != %s)' % (V['esc'], V['esc_ant']))
    V['nax_sb'] = ESP['axiom_report_sandbox']
    Vd = lambda k: str((core.get(k) or {}).get('verdict') or 'AUSENTE')
    for k in NOVOS:
        V[k] = Vd(k)
        if (core.get(k) or {}).get('all_verified') is not True or V[k] != ESP['vereditos_v380_do_ensaio'][k]:
            P.append('%s nao selado como no ensaio' % k)
    for k in PINADOS:
        if (core.get(k) or {}).get('all_verified') is not True or Vd(k) != ESP['vereditos_pinados_v379'].get(k):
            P.append('%s (pinado) mudou ou nao selou' % k)
    V['iald'] = Vd('the_iald_index')
    if (core.get('the_iald_index') or {}).get('all_verified') is not True:
        P.append('the_iald_index nao selado')
    V['qg'] = str(selo.get('qg_closure_verdict'))
    if V['qg'] != ESP['qg_closure_verdict_v379']:
        P.append('o gate MUDOU (%s)' % V['qg'])
    qg = core.get('qg_closure') or {}
    V['n18'] = sum(1 for fam in ('formal_flags', 'physics_flags', 'experiment_flags') for v in (qg.get(fam) or {}).values() if v is True)
    fr = (qg.get('gate') or {}).get('kernel_frontier') or {}
    V['remaining'] = ', '.join(fr.get('remaining') or []) or 'n/d'
    V['closed_cit'] = ', '.join(fr.get('closed_by_citation_v374') or []) or 'n/d'
    V['after_cit'] = fr.get('remaining_after_citation_v374')
    if V['after_cit'] != []:
        P.append('remaining_after_citation_v374 nao e [] (%s)' % V['after_cit'])
    V['ident_open'] = ', '.join(fr.get('physical_identifications_open') or []) or 'n/d'
    tt = core.get('the_tetelestai_declaration_v374') or {}
    V['ledger'] = ', '.join('%s %d' % (k, v) for k, v in (tt.get('ledger_counts') or {}).items())
    cf = core.get('tetelestai_conference_v376') or {}
    V['cf_counts'] = ', '.join('%s %s' % (k, v) for k, v in (cf.get('counts') or {}).items()); V['abertos'] = cf.get('open_items')
    if cf.get('consummated') is not True or V['abertos'] != []:
        P.append('a conferencia v376 (pinada) nao le consumada nesta rodada')
    # ---- os numeros da v380 (lidos do core: o modulo bancada_fases_5_6_7_v380)
    bf = core.get('bancada_fases_5_6_7_v380') or {}; f5 = bf.get('fase5') or {}; f6 = bf.get('fase6') or {}; f7 = bf.get('fase7') or {}; e4 = (bf.get('emenda_v4') or {}).get('todos_MAY') or {}; gb = bf.get('gw_bank') or {}
    va = f5.get('validacao') or {}; p5 = f5.get('P_sombra') or {}; k6 = f6.get('todos_KMS') or {}; o6 = f6.get('o4_KMS_cego') or {}; m6 = f6.get('todos_MAY') or {}
    V['h0_v'] = _f(va.get('H0'), 2); V['h0_s'] = _f(va.get('sigma_H0'), 2); V['h0_z'] = _f(va.get('z_vs_alvo'), 2); V['p5_z'] = _f(p5.get('z_delta'), 2)
    V['k6_a'] = _f(k6.get('a'), 3); V['k6_s'] = _f(k6.get('sigma_usado'), 3); V['k6_z1'] = _f(k6.get('z_excl_R1'), 1); V['k6_z2'] = _f(k6.get('z_excl_R2'), 1); V['k6_sys'] = _f(k6.get('sistematica_abs'), 3)
    V['o6_z1'] = _f(o6.get('z_excl_R1'), 1); V['o6_z2'] = _f(o6.get('z_excl_R2'), 1); V['m6_sys'] = _f(m6.get('sistematica_abs'), 2)
    V['v4_z2'] = _f(e4.get('z_excl_R2'), 1); V['v4_ctrl'] = _f(e4.get('controles_max_z'), 1)
    tz = f7.get('T_z_ganho') or {}; lb = f7.get('U_lnB_sombra_vs_acumulada') or {}; s7 = (f7.get('S_delta') or {}).get('moresco2020') or {}
    V['t7_diag'] = _f(tz.get('diagonal'), 2); V['t7_m20'] = _f(tz.get('moresco2020'), 2); V['u7_diag'] = _f(lb.get('diagonal'), 2); V['u7_m20'] = _f(lb.get('moresco2020'), 2); V['s7_z'] = _f(s7.get('z'), 2)
    V['gb_ok'] = gb.get('n_ok'); V['gb_n'] = gb.get('n_jobs'); V['n_erratas'] = len(bf.get('errata_beside_v380') or {})
    e5 = (bf.get('emenda_v5') or {}).get('todos_DEC') or {}; o5 = (bf.get('emenda_v5') or {}).get('o4_DEC_cego') or {}
    V['v5_z1'] = _f(e5.get('z_excl_R1'), 1); V['v5_z2'] = _f(e5.get('z_excl_R2'), 1); V['v5_o1'] = _f(o5.get('z_excl_R1'), 1); V['v5_o2'] = _f(o5.get('z_excl_R2'), 1); V['v5_r3p'] = _f(e5.get('poder_R3'), 1); V['v5_sys'] = _f(e5.get('sistematica_abs'), 3)
    # ---- os acrescimos do aferidor v380 (achados 1, 4, 5, 6, 10, 11): rotulo emitido e clausula V5; controle tau/2 de MAY na V3; subamostra O4; poder cego; banco por status; sistematica relativa
    ev5 = bf.get('emenda_v5') or {}; V['v5_r3lab'] = str(ev5.get('R3_rotulo_emitido') or 'AUSENTE').replace('TGL_ECHO_RADICAL_V3__', ''); V['v5_r3cp'] = _f(ev5.get('poder_R3_cego'), 2)
    V['v5_clausula'] = 'NÃO aplicada pelo pipeline (dito)' if ev5.get('clausula_v5_aplicada_pelo_pipeline') is False and ev5.get('clausula_v5_no_preregistro') is True else 'n/d'
    V['k6_n'] = k6.get('n_eventos'); V['o6_n'] = o6.get('n_eventos'); V['k6_sr1'] = _f(k6.get('sist_rel_R1'), 2); V['k6_sr2'] = _f(k6.get('sist_rel_R2'), 2)
    cm = f6.get('controles_MAY_v3_z') or {}; V['m6_c1'] = _f((cm.get('todos') or {}).get('x0.5'), 2); V['m6_c1o'] = _f((cm.get('o4') or {}).get('x0.5'), 2)
    V['m6_flag'] = 'NÃO gravada pelo pipeline (dito)' if f6.get('flag_delay_control_written_by_pipeline') is False else 'n/d'
    gbs = gb.get('status') or {}; V['gb_nan'] = gbs.get('NAN_IN_WINDOW'); V['gb_out'] = gbs.get('WINDOW_OUTSIDE_FILE'); V['n_crlf'] = len(bf.get('crlf_differs') or [])
    if 'KMS_PAIR_SQRT_BETA_AND_SIN2THETA_FALSIFIED_AT_DELAY_LAW' not in V['bancada_fases_5_6_7_v380'] or bf.get('all_verified') is not True:
        P.append('o modulo v380 nao selou como esperado')
    for tok in ('V5_CLAUSE_UNDERPOWERED_NOT_APPLIED_STATED', 'FLAG_NOT_WRITTEN_BY_PIPELINE_STATED', 'BLIND_O4_SUBSAMPLE_', 'ERRATA_BESIDE_6_PLUS_V378_1_PLUS_NOTE_1'):
        if tok not in V['bancada_fases_5_6_7_v380']:
            P.append('o veredito v380 nao carrega o token %s (aferidor)' % tok)
    if not all(k in selo for k in ('joint_coincidence_result_v3_verdict', 'd1_camb_v3_real_v366_verdict')):
        P.append('as chaves EV-06 nao estao no selo')
    V['um_version'] = str(selo.get('um_version'))
    if V['um_version'] != 'v380':
        P.append('selo.um_version != v380 (%s)' % V['um_version'])
    _mds = [os.path.join(nos, 'um_absoluto_forma_canonica.md'), os.path.join(nos, 'um_absoluto_manifest.md')]
    _car = all(os.path.exists(p) and '**Versão v380**' in open(p, encoding='utf-8', errors='replace').read() for p in _mds)
    V['md_carimbo'] = 'SIM (forma canônica + manifesto)' if _car else 'NÃO'
    if not _car:
        P.append('os .md emitidos nao trazem o carimbo v380')
    V['fse'] = selo.get('full_static_witness_exists')
    for k in LEITURAS:
        V[k] = str(selo.get(k) or 'AUSENTE')
        if V[k] == 'AUSENTE':
            P.append('leitura %s ausente do selo' % k)
    nst = selo.get('not_sealed_this_run') or {}
    V['formais'] = ', '.join(nst.get('formais') or []) or 'nenhum'
    proib = [k for k, mm in core.items() if isinstance(mm, dict) and (GUARDA.search(str(mm.get('verdict') or '')) or 'TGL_PROVED' in str(mm.get('verdict') or ''))]
    if proib:
        P.append('veredito proibido: %s' % proib)
    V['n_pin'] = len(ESP['vereditos_pinados_v379'])
    try:
        V['data'] = time.strftime('%d/%m/%Y', time.strptime(V['selo_ts'][:10], '%Y-%m-%d'))
    except ValueError:
        V['data'] = time.strftime('%d/%m/%Y')
    return V, P
