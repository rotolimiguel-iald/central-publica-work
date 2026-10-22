# -*- coding: utf-8 -*-
# LEITURA da rodada v383 -- SO LEITURA. Todo numero, hash e veredito sai daqui, LIDO do artefato (JSON selado, selo, stdout, kernel
# materializado, conferidor, pacote v383), nunca digitado. Usado por superficies_v383.py, manifesto_v383.py, patch_arvore_indice_v383.py, handoff_v383.py.
import os, re, json, glob, hashlib, time
HERE = os.path.dirname(os.path.abspath(__file__))
SP = os.path.dirname(HERE)
PK = os.path.join(SP, 'v383')
NOS_REAL = r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós'
FINAL_RE = re.compile(r'^\[selo\] colapso tipado: ')
TRAILER_RE = re.compile(r'^(exit=\d+|rc=\d+|RITO_RC=\d+|inicio |fim )')
NOVOS = ('the_ledger_of_charges_v383',)
PEDRAS = ('TheLedgerOfCharges', 'ThePsionAndTheViscosity')
LEITURAS = ('the_ledger_of_charges_reading_v383',)
PINADOS = ('physics_is_the_reading_v377', 'the_dissipation_law_v377', 'bancada_fases_v377', 'final_stone_reading_v377',
           'the_dissipation_law_with_contrast_v378', 'what_was_missed_v378', 'bancada_fase4_v378', 'the_elementary_reason_v379', 'bancada_fases_5_6_7_v380', 'the_matrix_rule_v381')
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
    assert ps, 'APLICADO_AO_CANONICO_*.json ausente no pacote v383'
    return json.load(open(ps[-1], encoding='utf-8')), ps[-1]


def _f(x, nd=2):
    return ('%.*f' % (nd, x)) if isinstance(x, (int, float)) else 'n/d'


def ler():
    P = []
    ESP = json.load(open(os.path.join(PK, 'ESPERADOS_v383.json'), encoding='utf-8'))
    ap, app = _aplicado()
    nos = os.environ.get('V383_NOS') or NOS_REAL
    V = {'nos': nos, 'aplicado_json': app}
    res = json.load(open(os.path.join(nos, 'um_absoluto.json'), encoding='utf-8'))
    selo = json.load(open(os.path.join(nos, 'um_absoluto_selo.json'), encoding='utf-8'))
    stp = os.path.join(nos, 'rodada_v383_stdout.txt')
    out = open(stp, encoding='utf-8', errors='replace').read()
    KT = os.path.join(nos, 'tgl_kernel')
    V['s16'] = sha(os.path.join(nos, 'um.py'))[:16]; V['umb'] = os.path.getsize(os.path.join(nos, 'um.py'))
    core = res['core']
    if not str((selo.get('sha256') or {}).get('um.py', '')).startswith(V['s16']):
        P.append('selo.sha256(um.py) != disco')
    V['base16'] = ap['backups']['um.py']['sha16']
    if V['base16'] != ESP['origem_sha16']:
        P.append('base lida (%s) != origem de ESPERADOS -- a v382 selada so no Nos (%s)' % (V['base16'], ESP['origem_sha16']))
    V['base_build16'] = ESP['base_build_sha16']; V['v382_16'] = ESP['v382_so_local_sha16']   # v383: a BASE do candidato (v381) e a v382 so local (a origem substituida no Nos)
    if V['base16'] != V['v382_16']:
        P.append('a origem substituida (%s) nao e a v382 so local de ESPERADOS (%s)' % (V['base16'], V['v382_16']))
    V['v382_stdout_no_nos'] = os.path.exists(os.path.join(nos, 'rodada_v382_stdout.txt'))
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
    V['rc'] = os.environ.get('V383_RC') or (mrc[-1] if mrc else 'NAO_LIDO')
    V['rcsrc'] = 'dito pela gerência (V383_RC)' if os.environ.get('V383_RC') else ('linha RITO_RC= do stdout (escrita pelo shell da gerência)' if mrc else 'ausente')
    if V['rc'] != '0':
        P.append('rc do rito nao lido como 0 (%s)' % V['rc'])
    hor = os.path.join(PK, 'rito_horarios_v383.txt')
    hh = open(hor, encoding='utf-8').read().split() if os.path.exists(hor) else []
    V['t0'] = hh[0] if hh else 'n/d'
    V['t1'] = hh[1] if len(hh) > 1 else time.strftime('%H:%M:%S', time.localtime(os.stat(stp).st_mtime))
    V['tsrc'] = 'horários gravados pelo shell da gerência' if len(hh) > 1 else 'fim = última modificação do stdout'
    V['tentativas'] = sorted(os.path.basename(p) for p in glob.glob(os.path.join(nos, 'rodada_v383_stdout_tentativa*.txt')))
    V['selo_ts'] = str(selo.get('timestamp'))
    ts_ap = '%s-%s-%s %s:%s:%s' % (ap['ts'][0:4], ap['ts'][4:6], ap['ts'][6:8], ap['ts'][9:11], ap['ts'][11:13], ap['ts'][13:15])
    if not (V['selo_ts'] >= ts_ap):
        P.append('o selo (%s) e anterior a instalacao da v383 (%s)' % (V['selo_ts'], ts_ap))
    confp = os.path.join(HERE, 'conferidor', 'conferencia_rito_v383.json'); confo = os.path.join(HERE, 'conferir_rito_v383_stdout.txt')
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
    _nomes = json.load(open(os.path.join(PK, 'AUDIT_NOMES_v383.json'), encoding='utf-8'))
    for n in PEDRAS:
        rel = 'TGLExt/%s.lean' % n; p = os.path.join(KT, *rel.split('/'))
        got = sha_txt16(p) if os.path.exists(p) else 'AUSENTE'
        V['pedras'][n] = {'sha16': got, 'n_print': len(_nomes.get(n, []))}
        if got != novos.get(rel):
            P.append('pedra %s materializada %s != esperada %s' % (n, got, novos.get(rel)))
    kf = core.get('kernel_formalization') or {}
    FL = [f for f, _ in ESP['bandeiras']]
    V['n_flags_on'] = sum(1 for f in FL if kf.get(f) is True); V['n_flags'] = len(FL)
    if V['n_flags_on'] != len(FL) or len(FL) != 32:
        P.append('bandeiras v383 acesas %d/%d' % (V['n_flags_on'], len(FL)))
    if not all(kf.get(f) is True for f in ESP['bandeiras_antigas']):
        P.append('bandeiras antigas (v377-v381) apagadas')
    V['gpc'] = {k: kf.get(k) for k in ('gpc_H2_smooth_modular_four_frame_discharged', 'gpc_H3_local_horizon_equilibrium_discharged', 'gpc_H3_horizon_data_produced')}
    if not all(v is True for v in V['gpc'].values()):
        P.append('bandeiras gpc_ nao todas True: %s' % V['gpc'])
    V['termo'] = {k: kf.get(k) for k in TERMO}
    V['hvals'] = '/'.join(str(v) for v in V['termo'].values())
    if any(v is not False for v in V['termo'].values()):
        P.append('POR TERMO nao False: %s' % V['hvals'])
    lad = core.get('external_ladder') or {}
    V['esc'] = '%s/%s' % (lad.get('n_theorems_clean'), lad.get('n_theorems_expected'))
    V['esc_ant'] = '%d/%d' % tuple(ESP['escada_v381']); V['nax'] = len(kf.get('axiom_report') or {}); V['nax_ant'] = ESP['axiom_report_v381']
    V['nax_sb'] = ESP['axiom_report_sandbox']
    Vd = lambda k: str((core.get(k) or {}).get('verdict') or 'AUSENTE')
    for k in NOVOS:
        V[k] = Vd(k)
        if (core.get(k) or {}).get('all_verified') is not True or V[k] != ESP['vereditos_v383_do_ensaio'][k]:
            P.append('%s nao selado como no ensaio' % k)
    for k in PINADOS:
        if (core.get(k) or {}).get('all_verified') is not True or Vd(k) != ESP['vereditos_pinados_v381'].get(k):
            P.append('%s (pinado) mudou ou nao selou' % k)
    V['iald'] = Vd('the_iald_index')
    if (core.get('the_iald_index') or {}).get('all_verified') is not True:
        P.append('the_iald_index nao selado')
    V['qg'] = str(selo.get('qg_closure_verdict'))
    if V['qg'] != ESP['qg_closure_verdict_v381']:
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
    # ---- os numeros da v383 (lidos do core: o modulo the_ledger_of_charges_v383)
    lc = core.get('the_ledger_of_charges_v383') or {}; rt = lc.get('runtime') or {}; pr = lc.get('preregistration') or {}; ct = lc.get('counts') or {}; bs = lc.get('by_side') or {}
    V['beta'] = _f(rt.get('beta_core'), 12); V['law'] = _f(rt.get('law_alpha_sqrt_e'), 12); V['theta'] = _f(rt.get('theta_M'), 9)
    V['facew'] = _f(rt.get('face_weight_cos2'), 12); V['reflw'] = _f(rt.get('reflection_weight_sin2'), 12); V['trans'] = _f(rt.get('transmitted_t1_g1'), 9); V['charged'] = _f(rt.get('charged_t1_g1'), 9); V['visc'] = _f(rt.get('viscosity_coefficient_g1'), 12)
    V['n_ledger'] = len(lc.get('ledger') or []); V['counts'] = ', '.join('%s %s' % (k, v) for k, v in ct.items()); V['by_side'] = '; '.join('%s: %s' % (sd, ', '.join('%s %s' % (k, v) for k, v in d.items() if v)) for sd, d in bs.items())
    V['by_how'] = ', '.join('%s %s' % (k, v) for k, v in (lc.get('by_how') or {}).items()); V['n_in_rule'] = lc.get('n_in_rule'); V['n_beside'] = lc.get('n_beside')
    V['counts_in_rule'] = ', '.join('%s %s' % (k, v) for k, v in (lc.get('counts_in_rule') or {}).items() if v)
    V['ledger_ids'] = ', '.join('%s (%s, %s)' % (c.get('id'), c.get('side'), c.get('outcome')) for c in (lc.get('ledger') or []))
    V['kf_on'] = sum(1 for v in (lc.get('kernel_flags') or {}).values() if v); V['kf_n'] = len(lc.get('kernel_flags') or {})
    V['pr_json16'] = str((pr.get('sha256_read') or {}).get('json') or 'AUSENTE')[:16]; V['pr_md16'] = str((pr.get('sha256_read') or {}).get('md') or 'AUSENTE')[:16]; V['pr_id'] = str(pr.get('identificador') or 'AUSENTE'); V['pr_seq'] = str(pr.get('mapa_seq') or 'n/d')
    V['pr_super'] = str(pr.get('supersede') or 'n/d')
    _lab = V['pr_id'].rsplit('_V', 1)[-1].split('_') if '_V' in V['pr_id'] else []
    V['pr_label'] = ('V' + '.'.join(_lab)) if (len(_lab) == 2 and all(x.isdigit() for x in _lab)) else 'AUSENTE'
    if V['pr_label'] == 'AUSENTE':
        P.append('o identificador do pre-registro nao da o rotulo da versao (%s)' % V['pr_id'])
    V['r2_gamma'] = ('%.2e' % rt['R2_gamma_100hz_per_s']) if isinstance(rt.get('R2_gamma_100hz_per_s'), (int, float)) else 'n/d'; V['r2_acc'] = ('%.2e' % rt['R2_gamma_accumulated_1gpc']) if isinstance(rt.get('R2_gamma_accumulated_1gpc'), (int, float)) else 'n/d'
    V['fsn'] = str(lc.get('final_step_name_proposed') or 'AUSENTE'); V['gate_unchanged'] = lc.get('gate_unchanged')
    _er = lc.get('echo_routes_outside_the_ledger') or {}; V['rot_n'] = _er.get('n'); V['rot_exc'] = _er.get('excluded_by_data'); V['rot_inc'] = _er.get('inconclusive')
    V['rot_ids'] = ', '.join('%s %s' % (r.get('id'), r.get('state')) for r in (_er.get('routes') or []))
    if V['rot_n'] != 9 or (V['rot_exc'] or 0) + (V['rot_inc'] or 0) != 9 or _er.get('not_charges_of_the_theory') is not True or _er.get('sources_in_core_ok') is not True:
        P.append('as rotas do eco fora do livro nao fecham (%s)' % {k: _er.get(k) for k in ('n', 'excluded_by_data', 'inconclusive', 'not_charges_of_the_theory', 'sources_in_core_ok')})
    _bl = lc.get('base_and_local_seal') or {}
    if _bl.get('base') != 'v381' or _bl.get('v382_local_only_sha16') != V['v382_16']:
        P.append('a base declarada (%s) ou a v382 so local (%s) nao batem' % (_bl.get('base'), _bl.get('v382_local_only_sha16')))
    V['decisao'] = str((lc.get('operator_decision_20261002') or {}).get('verbatim') or 'AUSENTE')
    if V['decisao'] != 'prefiro a primeira opção':
        P.append('a decisao do operador nao esta no modulo, verbatim (%s)' % V['decisao'])
    if ('THE_TGL_IS_OPTICS_NOT_SEMI_BOTH_SIDES_READ' not in V['the_ledger_of_charges_v383'] or 'KERNEL_32_OF_32' not in V['the_ledger_of_charges_v383'] or 'NOT_A_CONFIRMATION' not in V['the_ledger_of_charges_v383']
            or 'THE_9_ECHO_ROUTES_ARE_NOT_CHARGES_OF_THE_THEORY' not in V['the_ledger_of_charges_v383'] or 'BASE_V381' not in V['the_ledger_of_charges_v383']):
        P.append('as pedras v383 nao selaram como esperado')
    if V['n_ledger'] != 11 or V['kf_on'] != 32 or V['kf_n'] != 32 or pr.get('read_ok') is not True or lc.get('gate_unchanged') is not True:
        P.append('o livro lido nao tem onze cobrancas / 32 bandeiras / pre-registro %s por hash / gate inalterado (%d; %d/%d; %s; %s)' % (V['pr_label'], V['n_ledger'], V['kf_on'], V['kf_n'], pr.get('read_ok'), lc.get('gate_unchanged')))
    if not all(c.get('outcome_ok') and c.get('matches_preregistration') for c in (lc.get('ledger') or [])) or lc.get('n_token_in_core') != lc.get('n_with_core_key'):
        P.append('alguma cobranca do livro nao bate com o core (pelo modo dito) ou com o pre-registro %s' % V['pr_label'])
    V['um_version'] = str(selo.get('um_version'))
    if V['um_version'] != 'v383':
        P.append('selo.um_version != v383 (%s)' % V['um_version'])
    _mds = [os.path.join(nos, 'um_absoluto_forma_canonica.md'), os.path.join(nos, 'um_absoluto_manifest.md')]
    _car = all(os.path.exists(p) and '**Versão v383**' in open(p, encoding='utf-8', errors='replace').read() for p in _mds)
    V['md_carimbo'] = 'SIM (forma canônica + manifesto)' if _car else 'NÃO'
    if not _car:
        P.append('os .md emitidos nao trazem o carimbo v383')
    V['n_loc'] = V['pedras'].get('TheLedgerOfCharges', {}).get('n_print'); V['n_psv'] = V['pedras'].get('ThePsionAndTheViscosity', {}).get('n_print')
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
    V['n_pin'] = len(ESP['vereditos_pinados_v381'])
    try:
        V['data'] = time.strftime('%d/%m/%Y', time.strptime(V['selo_ts'][:10], '%Y-%m-%d'))
    except ValueError:
        V['data'] = time.strftime('%d/%m/%Y')
    return V, P
