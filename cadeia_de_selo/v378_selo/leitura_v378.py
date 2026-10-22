# -*- coding: utf-8 -*-
# LEITURA da rodada v378 -- SO LEITURA. Todo numero, hash e veredito sai daqui, LIDO do artefato (JSON selado, selo, stdout, kernel
# materializado, conferidor, pacote v378), nunca digitado. Usado por superficies_v378.py, manifesto_v378.py, patch_arvore_indice_v378.py, handoff_v378.py.
import os, re, json, glob, hashlib, time
HERE = os.path.dirname(os.path.abspath(__file__))
SP = os.path.dirname(HERE)
PK = os.path.join(SP, 'v378')
NOS_REAL = r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós'
FINAL_RE = re.compile(r'^\[selo\] colapso tipado: ')
TRAILER_RE = re.compile(r'^(exit=\d+|rc=\d+|RITO_RC=\d+|inicio |fim )')
NOVOS = ('the_dissipation_law_with_contrast_v378', 'what_was_missed_v378', 'bancada_fase4_v378')
PEDRAS = ('TheFlowLawContrast',)
LEITURAS = ('the_contrast_and_deviation_reading_v378',)
PINADOS_V377 = ('physics_is_the_reading_v377', 'the_dissipation_law_v377', 'bancada_fases_v377', 'final_stone_reading_v377')
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
    assert ps, 'APLICADO_AO_CANONICO_*.json ausente no pacote v378'
    return json.load(open(ps[-1], encoding='utf-8')), ps[-1]


def _f(x, nd=2):
    return ('%.*f' % (nd, x)) if isinstance(x, (int, float)) else 'n/d'


def ler():
    P = []
    ESP = json.load(open(os.path.join(PK, 'ESPERADOS_v378.json'), encoding='utf-8'))
    ap, app = _aplicado()
    nos = os.environ.get('V378_NOS') or NOS_REAL
    V = {'nos': nos, 'aplicado_json': app}
    res = json.load(open(os.path.join(nos, 'um_absoluto.json'), encoding='utf-8'))
    selo = json.load(open(os.path.join(nos, 'um_absoluto_selo.json'), encoding='utf-8'))
    stp = os.path.join(nos, 'rodada_v378_stdout.txt')
    out = open(stp, encoding='utf-8', errors='replace').read()
    KT = os.path.join(nos, 'tgl_kernel')
    V['s16'] = sha(os.path.join(nos, 'um.py'))[:16]; V['umb'] = os.path.getsize(os.path.join(nos, 'um.py'))
    core = res['core']
    if not str((selo.get('sha256') or {}).get('um.py', '')).startswith(V['s16']):
        P.append('selo.sha256(um.py) != disco')
    V['base16'] = ap['backups']['um.py']['sha16']
    if V['base16'] != ESP['origem_sha16']:
        P.append('base lida (%s) != origem v377 de ESPERADOS (%s)' % (V['base16'], ESP['origem_sha16']))
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
    V['rc'] = os.environ.get('V378_RC') or (mrc[-1] if mrc else 'NAO_LIDO')
    V['rcsrc'] = 'dito pela gerência (V378_RC)' if os.environ.get('V378_RC') else ('linha RITO_RC= do stdout (escrita pelo shell da gerência)' if mrc else 'ausente')
    if V['rc'] != '0':
        P.append('rc do rito nao lido como 0 (%s)' % V['rc'])
    hor = os.path.join(PK, 'rito_horarios_v378.txt')
    hh = open(hor, encoding='utf-8').read().split() if os.path.exists(hor) else []
    V['t0'] = hh[0] if hh else 'n/d'
    V['t1'] = hh[1] if len(hh) > 1 else time.strftime('%H:%M:%S', time.localtime(os.stat(stp).st_mtime))
    V['tsrc'] = 'horários gravados pelo shell da gerência' if len(hh) > 1 else 'fim = última modificação do stdout'
    V['tentativas'] = sorted(os.path.basename(p) for p in glob.glob(os.path.join(nos, 'rodada_v378_stdout_tentativa*.txt')))
    V['selo_ts'] = str(selo.get('timestamp'))
    ts_ap = '%s-%s-%s %s:%s:%s' % (ap['ts'][0:4], ap['ts'][4:6], ap['ts'][6:8], ap['ts'][9:11], ap['ts'][11:13], ap['ts'][13:15])
    if not (V['selo_ts'] >= ts_ap):
        P.append('o selo (%s) e anterior a instalacao da v378 (%s)' % (V['selo_ts'], ts_ap))
    confp = os.path.join(HERE, 'conferidor', 'conferencia_rito_v378.json'); confo = os.path.join(HERE, 'conferir_rito_v378_stdout.txt')
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
    _nomes = json.load(open(os.path.join(PK, 'AUDIT_NOMES_v378.json'), encoding='utf-8'))
    for n in PEDRAS:
        rel = 'TGLExt/%s.lean' % n; p = os.path.join(KT, *rel.split('/'))
        got = sha_txt16(p) if os.path.exists(p) else 'AUSENTE'
        V['pedras'][n] = {'sha16': got, 'n_print': len(_nomes.get(n, []))}
        if got != novos.get(rel):
            P.append('pedra %s materializada %s != esperada %s' % (n, got, novos.get(rel)))
    kf = core.get('kernel_formalization') or {}
    FL = [f for f, _ in ESP['bandeiras']]
    V['n_flags_on'] = sum(1 for f in FL if kf.get(f) is True); V['n_flags'] = len(FL)
    if V['n_flags_on'] != len(FL) or len(FL) != 20:
        P.append('bandeiras v378 acesas %d/%d' % (V['n_flags_on'], len(FL)))
    if not all(kf.get(f) is True for f in ESP['bandeiras_v377']):
        P.append('bandeiras v377 apagadas')
    V['gpc'] = {k: kf.get(k) for k in ('gpc_H2_smooth_modular_four_frame_discharged', 'gpc_H3_local_horizon_equilibrium_discharged', 'gpc_H3_horizon_data_produced')}
    if not all(v is True for v in V['gpc'].values()):
        P.append('bandeiras gpc_ nao todas True: %s' % V['gpc'])
    V['termo'] = {k: kf.get(k) for k in TERMO}
    V['hvals'] = '/'.join(str(v) for v in V['termo'].values())
    if any(v is not False for v in V['termo'].values()):
        P.append('POR TERMO nao False: %s' % V['hvals'])
    lad = core.get('external_ladder') or {}
    V['esc'] = '%s/%s' % (lad.get('n_theorems_clean'), lad.get('n_theorems_expected'))
    V['esc_ant'] = '%d/%d' % tuple(ESP['escada_v377']); V['nax'] = len(kf.get('axiom_report') or {}); V['nax_ant'] = ESP['axiom_report_v377']
    V['nax_sb'] = ESP['axiom_report_sandbox']
    Vd = lambda k: str((core.get(k) or {}).get('verdict') or 'AUSENTE')
    for k in NOVOS:
        V[k] = Vd(k)
        if (core.get(k) or {}).get('all_verified') is not True or V[k] != ESP['vereditos_v378_do_ensaio'][k]:
            P.append('%s nao selado como no ensaio' % k)
    for k in PINADOS_V377:
        if (core.get(k) or {}).get('all_verified') is not True or Vd(k) != ESP['vereditos_pinados_v377'].get(k):
            P.append('%s (v377, pinado) mudou ou nao selou' % k)
    V['iald'] = Vd('the_iald_index')
    if (core.get('the_iald_index') or {}).get('all_verified') is not True:
        P.append('the_iald_index nao selado')
    V['qg'] = str(selo.get('qg_closure_verdict'))
    if V['qg'] != ESP['qg_closure_verdict_v377']:
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
    # ---- os numeros da v378
    dl = core.get('the_dissipation_law_with_contrast_v378') or {}; wm = core.get('what_was_missed_v378') or {}; b4 = core.get('bancada_fase4_v378') or {}
    V['Ka'] = _f(dl.get('K_D1a_runtime'), 6); V['Kb'] = _f(dl.get('K_D1b_runtime'), 6); V['Ib'] = _f(dl.get('I_b_closed_form'), 4); V['Nstar'] = _f(dl.get('register_N_star_nats'), 4)
    V['gmin'] = _f(dl.get('min_1_plus_w_eff_grid'), 4); V['dpred'] = _f(dl.get('predicted_deviation_over_beta_D1b'), 4); V['pernat'] = _f(dl.get('per_nat_cost_D1b'), 5)
    V['H0b'] = _f(dl.get('H0_local_D1b_from_planck'), 2); V['H0a'] = _f(dl.get('H0_local_D1a_from_planck'), 2); V['Ezs'] = _f(dl.get('E_z_star'), 1)
    V['coma_v378'] = str(dl.get('coma_v39_flow_layer_kernel_v378_beside'))
    if 'TheFlowLawContrast' not in V['coma_v378']:
        P.append('a chave ao lado no modulo de Coma nao leu (%s)' % V['coma_v378'])
    V['w_seis'] = _f((wm.get('shadow_readers_planck_lcdm_D1b') or {}).get('z_comb')); V['w_novos'] = _f((wm.get('new_readers_planck_lcdm_D1b') or {}).get('z_comb'))
    V['w_emp'] = _f(wm.get('stacked_control_D1b_z')); V['w_h'] = str((wm.get('reanalysis_hashes') or {}).get('sha16_bytes')); V['w_cega'] = str(wm.get('reanalysis_declared_blind'))
    Pl = b4.get('P_ladder_d1b') or {}; Ti = b4.get('T_intermediate_d1b') or {}; Sj = b4.get('S_joint_d1b') or {}; Kc = b4.get('stacked_control') or {}; pT = b4.get('posterior_T') or {}; pP = b4.get('posterior_P') or {}
    V['P_delta'] = _f(Pl.get('delta'), 5); V['P_sigma'] = _f(Pl.get('sigma_delta'), 5); V['P_z'] = _f(Pl.get('z_delta')); V['P_pull'] = _f(Pl.get('pull')); V['P_lnB'] = _f((Pl.get('lnB') or {}).get('tgl_vs_lcdm'))
    V['P_lnBl'] = _f((Pl.get('lnB') or {}).get('tgl_vs_livre')); V['P_H0'] = _f(Pl.get('H0_bg')); V['P_K'] = _f(Pl.get('K'), 5); V['P_H0l'] = _f(Pl.get('H0_local'))
    V['T_bhat'] = _f(Ti.get('beta_livre'), 5); V['T_delta'] = _f(Ti.get('delta'), 5); V['T_sigma'] = _f(Ti.get('sigma_delta'), 5); V['T_z'] = _f(Ti.get('z_delta')); V['T_gain'] = _f(Ti.get('z_ganho_da_lei')); V['T_lnB'] = _f((Ti.get('lnB') or {}).get('tgl_vs_lcdm'))
    V['T_frac'] = _f(pT.get('fracao_beta_acima_de_beta_tgl'), 3); V['T_frac0'] = _f(pT.get('fracao_beta_acima_de_zero'), 3); V['P_frac'] = _f(pP.get('fracao_beta_acima_de_beta_tgl'), 3)
    V['S_z'] = _f(Sj.get('z_delta')); V['ctrl_z'] = _f(Kc.get('z_delta')); V['poder'] = _f(b4.get('power_prior_cc_sigma')); V['cc_n'] = str(b4.get('cc_n'))
    V['f4_ver'] = str(b4.get('veredito_fase4')); V['f4_verT'] = str(b4.get('veredito_T'))
    hs = b4.get('hashes') or {}
    V['bancada_hashes'] = '; '.join('%s `%s`' % (v.get('file'), v.get('sha16_bytes')) for v in hs.values())
    if not hs or b4.get('all_verified') is not True:
        P.append('a Fase 4 nao leu por hash nesta rodada')
    V['um_version'] = str(selo.get('um_version'))
    if V['um_version'] != 'v378':
        P.append('selo.um_version != v378 (%s)' % V['um_version'])
    _mds = [os.path.join(nos, 'um_absoluto_forma_canonica.md'), os.path.join(nos, 'um_absoluto_manifest.md')]
    _car = all(os.path.exists(p) and '**Versão v378**' in open(p, encoding='utf-8', errors='replace').read() for p in _mds)
    V['md_carimbo'] = 'SIM (forma canônica + manifesto)' if _car else 'NÃO'
    if not _car:
        P.append('os .md emitidos nao trazem o carimbo v378')
    V['n_dlc'] = V['pedras'].get('TheFlowLawContrast', {}).get('n_print')
    if 'FLOW_LAW_WITH_CONTRAST_TYPED' not in V['the_dissipation_law_with_contrast_v378'] or 'READ_BY_HASH' not in V['bancada_fase4_v378']:
        P.append('as pedras/modulos v378 nao selaram como esperado')
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
    V['n_pin'] = len(ESP['vereditos_pinados_v377'])
    try:
        V['data'] = time.strftime('%d/%m/%Y', time.strptime(V['selo_ts'][:10], '%Y-%m-%d'))
    except ValueError:
        V['data'] = time.strftime('%d/%m/%Y')
    return V, P
