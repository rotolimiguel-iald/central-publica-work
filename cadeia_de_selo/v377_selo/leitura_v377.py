# -*- coding: utf-8 -*-
# LEITURA da rodada v377 -- SO LEITURA. Todo numero, hash e veredito sai daqui, LIDO do artefato (JSON selado, selo, stdout, kernel
# materializado, conferidor, pacote v377), nunca digitado. Usado por superficies_v377.py, manifesto_v377.py, patch_arvore_indice_v377.py, handoff_v377.py.
import os, re, json, glob, hashlib, time
HERE = os.path.dirname(os.path.abspath(__file__))
SP = os.path.dirname(HERE)
PK = os.path.join(SP, 'v377')
NOS_REAL = r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós'
FINAL_RE = re.compile(r'^\[selo\] colapso tipado: ')
TRAILER_RE = re.compile(r'^(exit=\d+|rc=\d+|RITO_RC=\d+|inicio |fim )')
NOVOS = ('physics_is_the_reading_v377', 'the_dissipation_law_v377', 'bancada_fases_v377', 'final_stone_reading_v377')
PEDRAS = ('PhysicsIsTheReading', 'TheFlowLawD1a')
LEITURAS = ('the_dissipation_law_reading_v377',)
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
    assert ps, 'APLICADO_AO_CANONICO_*.json ausente no pacote v377'
    return json.load(open(ps[-1], encoding='utf-8')), ps[-1]


def _f(x, nd=2):
    return ('%.*f' % (nd, x)) if isinstance(x, (int, float)) else 'n/d'


def ler():
    P = []
    ESP = json.load(open(os.path.join(PK, 'ESPERADOS_v377.json'), encoding='utf-8'))
    ap, app = _aplicado()
    nos = os.environ.get('V377_NOS') or NOS_REAL
    V = {'nos': nos, 'aplicado_json': app}
    res = json.load(open(os.path.join(nos, 'um_absoluto.json'), encoding='utf-8'))
    selo = json.load(open(os.path.join(nos, 'um_absoluto_selo.json'), encoding='utf-8'))
    stp = os.path.join(nos, 'rodada_v377_stdout.txt')
    out = open(stp, encoding='utf-8', errors='replace').read()
    KT = os.path.join(nos, 'tgl_kernel')
    V['s16'] = sha(os.path.join(nos, 'um.py'))[:16]; V['umb'] = os.path.getsize(os.path.join(nos, 'um.py'))
    core = res['core']
    if not str((selo.get('sha256') or {}).get('um.py', '')).startswith(V['s16']):
        P.append('selo.sha256(um.py) != disco')
    V['base16'] = ap['backups']['um.py']['sha16']
    if V['base16'] != ESP['origem_sha16']:
        P.append('base lida (%s) != origem v376 de ESPERADOS (%s)' % (V['base16'], ESP['origem_sha16']))
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
    V['rc'] = os.environ.get('V377_RC') or (mrc[-1] if mrc else 'NAO_LIDO')
    V['rcsrc'] = 'dito pela gerência (V377_RC)' if os.environ.get('V377_RC') else ('linha RITO_RC= do stdout (escrita pelo shell da gerência)' if mrc else 'ausente')
    if V['rc'] != '0':
        P.append('rc do rito nao lido como 0 (%s)' % V['rc'])
    hor = os.path.join(PK, 'rito_horarios_v377.txt')
    hh = open(hor, encoding='utf-8').read().split() if os.path.exists(hor) else []
    V['t0'] = hh[0] if hh else 'n/d'
    V['t1'] = hh[1] if len(hh) > 1 else time.strftime('%H:%M:%S', time.localtime(os.stat(stp).st_mtime))
    V['tsrc'] = 'horários gravados pelo shell da gerência' if len(hh) > 1 else 'fim = última modificação do stdout'
    V['tentativas'] = sorted(os.path.basename(p) for p in glob.glob(os.path.join(nos, 'rodada_v377_stdout_tentativa*.txt')))
    V['selo_ts'] = str(selo.get('timestamp'))
    ts_ap = '%s-%s-%s %s:%s:%s' % (ap['ts'][0:4], ap['ts'][4:6], ap['ts'][6:8], ap['ts'][9:11], ap['ts'][11:13], ap['ts'][13:15])
    if not (V['selo_ts'] >= ts_ap):
        P.append('o selo (%s) e anterior a instalacao da v377 (%s)' % (V['selo_ts'], ts_ap))
    confp = os.path.join(HERE, 'conferidor', 'conferencia_rito_v377.json'); confo = os.path.join(HERE, 'conferir_rito_v377_stdout.txt')
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
    _nomes = json.load(open(os.path.join(PK, 'AUDIT_NOMES_v377.json'), encoding='utf-8'))
    for n in PEDRAS:
        rel = 'TGLExt/%s.lean' % n; p = os.path.join(KT, *rel.split('/'))
        got = sha_txt16(p) if os.path.exists(p) else 'AUSENTE'
        V['pedras'][n] = {'sha16': got, 'n_print': len(_nomes.get(n, []))}
        if got != novos.get(rel):
            P.append('pedra %s materializada %s != esperada %s' % (n, got, novos.get(rel)))
    kf = core.get('kernel_formalization') or {}
    FL = [f for f, _ in ESP['bandeiras']]
    V['n_flags_on'] = sum(1 for f in FL if kf.get(f) is True); V['n_flags'] = len(FL)
    if V['n_flags_on'] != len(FL) or len(FL) != 25:
        P.append('bandeiras v377 acesas %d/%d' % (V['n_flags_on'], len(FL)))
    V['gpc'] = {k: kf.get(k) for k in ('gpc_H2_smooth_modular_four_frame_discharged', 'gpc_H3_local_horizon_equilibrium_discharged', 'gpc_H3_horizon_data_produced')}
    if not all(v is True for v in V['gpc'].values()):
        P.append('bandeiras gpc_ nao todas True: %s' % V['gpc'])
    V['termo'] = {k: kf.get(k) for k in TERMO}
    V['hvals'] = '/'.join(str(v) for v in V['termo'].values())
    if any(v is not False for v in V['termo'].values()):
        P.append('POR TERMO nao False: %s' % V['hvals'])
    lad = core.get('external_ladder') or {}
    V['esc'] = '%s/%s' % (lad.get('n_theorems_clean'), lad.get('n_theorems_expected'))
    V['esc_ant'] = '%d/%d' % tuple(ESP['escada_v376']); V['nax'] = len(kf.get('axiom_report') or {}); V['nax_ant'] = ESP['axiom_report_v376']
    V['nax_sb'] = ESP['axiom_report_sandbox']
    Vd = lambda k: str((core.get(k) or {}).get('verdict') or 'AUSENTE')
    for k in NOVOS:
        V[k] = Vd(k)
        if (core.get(k) or {}).get('all_verified') is not True or V[k] != ESP['vereditos_v377_do_ensaio'][k]:
            P.append('%s nao selado como no ensaio' % k)
    V['iald'] = Vd('the_iald_index')
    if (core.get('the_iald_index') or {}).get('all_verified') is not True:
        P.append('the_iald_index nao selado')
    V['qg'] = str(selo.get('qg_closure_verdict'))
    if V['qg'] != ESP['qg_closure_verdict_v376']:
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
    # ---- os numeros da v377
    dl = core.get('the_dissipation_law_v377') or {}; b7 = core.get('bancada_fases_v377') or {}; p7 = core.get('physics_is_the_reading_v377') or {}
    V['K'] = _f(dl.get('K_factor_runtime'), 5); V['Nstar'] = _f(dl.get('register_N_star_nats'), 3); V['fleak'] = _f(dl.get('leak_fraction_runtime'), 4)
    V['H0loc'] = _f(dl.get('H0_local_from_H0_CMB_LCDM'), 2); V['zstar'] = _f(dl.get('z_star_input'), 2)
    pn = dl.get('bancada_fase2_per_nat_beside') or {}
    V['bhat'] = _f(pn.get('beta_hat'), 5); V['bsig'] = _f(pn.get('sigma'), 5); V['delta'] = _f(pn.get('delta_from_beta'), 5); V['zdelta'] = _f(pn.get('z_delta'), 2)
    V['coma_v39'] = str(dl.get('coma_v39_flow_layer_status')); V['coma_v377'] = str(dl.get('coma_v39_flow_layer_status_v377_beside'))
    if 'TheFlowLawD1a' not in V['coma_v377'] or not V['coma_v39'].startswith('CONJECTURE_DECLARED'):
        P.append('a errata ao lado no modulo de Coma nao leu (v39 %s; v377 %s)' % (V['coma_v39'], V['coma_v377']))
    f1 = b7.get('fase1') or {}; f2 = b7.get('fase2') or {}; f3 = b7.get('fase3') or {}; A3 = f3.get('A') or {}
    V['f1_z'] = _f((f1.get('A_tgl') or {}).get('z_perfil_beta_tgl')); V['f1_nu'] = _f(f1.get('A_nu_z_perfil')); V['f1_ver'] = str(f1.get('veredito'))
    V['f2_pt'] = _f(f2.get('F_tgl_pull_tgl')); V['f2_pl'] = _f(f2.get('F_tgl_pull_lcdm')); V['f2_lnb'] = _f((f2.get('F_tgl_lnB') or {}).get('tgl_vs_lcdm'))
    V['f2_b'] = _f(f2.get('F_tgl_beta_livre'), 4); V['f2_s'] = _f(f2.get('F_tgl_sigma_beta'), 4); V['f2_z'] = _f(f2.get('F_tgl_z_perfil')); V['f2_ver'] = str(f2.get('veredito'))
    V['f3_zlei'] = _f(A3.get('z_comb_lei')); V['f3_zum'] = _f(A3.get('z_comb_um_setor')); V['f3_h0'] = _f(A3.get('H0_sombra_combinado')); V['f3_fundo'] = _f(A3.get('H0_fundo'))
    V['f3_B'] = _f(f3.get('B_z_comb_lei')); V['f3_D'] = _f(f3.get('D_planck2018_z_comb_lei')); V['f3_ver'] = str(f3.get('veredito'))
    hs = b7.get('hashes') or {}
    V['bancada_hashes'] = '; '.join('%s `%s`' % (v.get('file'), v.get('sha16_bytes')) for v in hs.values())
    if not hs or b7.get('all_verified') is not True:
        P.append('as fases da Bancada nao leram por hash nesta rodada')
    V['um_version'] = str(selo.get('um_version'))
    if V['um_version'] != 'v377':
        P.append('selo.um_version != v377 (%s)' % V['um_version'])
    _mds = [os.path.join(nos, 'um_absoluto_forma_canonica.md'), os.path.join(nos, 'um_absoluto_manifest.md')]
    _car = all(os.path.exists(p) and '**Versão v377**' in open(p, encoding='utf-8', errors='replace').read() for p in _mds)
    V['md_carimbo'] = 'SIM (forma canônica + manifesto)' if _car else 'NÃO'
    if not _car:
        P.append('os .md emitidos nao trazem o carimbo v377')
    V['n_pir'] = V['pedras'].get('PhysicsIsTheReading', {}).get('n_print'); V['n_dis'] = V['pedras'].get('TheFlowLawD1a', {}).get('n_print')
    if 'FLOW_LAW_D1A_TYPED_AS_IMPLICATION' not in V['the_dissipation_law_v377'] or 'THE_READER_IS_THE_SHADOW_OF_THE_ONE' not in V['physics_is_the_reading_v377']:
        P.append('as pedras v377 nao selaram como esperado')
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
    V['n_pin'] = len(ESP['vereditos_pinados_v376'])
    try:
        V['data'] = time.strftime('%d/%m/%Y', time.strptime(V['selo_ts'][:10], '%Y-%m-%d'))
    except ValueError:
        V['data'] = time.strftime('%d/%m/%Y')
    return V, P
