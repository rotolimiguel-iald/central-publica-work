# -*- coding: utf-8 -*-
# A LEITURA da rodada v387 (molde: leitura_v386.py, enxuta): SO LEITURA do Nos, do pacote (work\v387_pacote) e dos V1 da Bancada. Devolve (V, PROBLEMAS):
# V = os numeros, hashes e vereditos LIDOS (nada digitado), para os textos das superficies; PROBLEMAS nao vazio => a cadeia PARA (nada se escreve).
import glob, hashlib, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
PK = os.path.join(os.path.dirname(HERE), "v387_pacote")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
FINAL_RE = re.compile(r'^\[selo\] colapso tipado: ')
TRAILER_RE = re.compile(r'^(exit=\d+|rc=\d+|RITO_RC=\S+|inicio |fim )')
GUARDA = re.compile('(?<!NOT_)(?<!UN)' + 'CONF' + 'IRMED|(?<!AP)PRO' + 'VED_BY|TGL_PRO' + 'VED')
REG = ("three_stress_tests_v387", "hubble_ratio_v387", "primordial_v387", "retrodiction_reading_v387")
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()


def _aplicado():
    ps = sorted(glob.glob(os.path.join(PK, 'APLICADO_AO_CANONICO_*.json')))
    assert ps, 'APLICADO_AO_CANONICO_*.json ausente no pacote v387'
    return json.load(open(ps[-1], encoding='utf-8')), ps[-1]


def ler():
    P = []
    ESP = json.load(open(os.path.join(PK, 'ESPERADOS_v387.json'), encoding='utf-8'))
    CM = json.load(open(os.path.join(PK, 'CANDIDATO_v387.json'), encoding='utf-8'))
    ap, app = _aplicado()
    res = json.load(open(os.path.join(NOS, 'um_absoluto.json'), encoding='utf-8')); core = res['core']
    selo = json.load(open(os.path.join(NOS, 'um_absoluto_selo.json'), encoding='utf-8'))
    stp = os.path.join(NOS, 'rodada_v387_stdout.txt')
    out = open(stp, encoding='utf-8', errors='replace').read() if os.path.exists(stp) else ''
    V = {'nos': NOS, 'aplicado_json': app}
    if not out:
        P.append('rodada_v387_stdout.txt ausente ou vazio')
    V['s64'] = sha(os.path.join(NOS, 'um.py')); V['s16'] = V['s64'][:16]; V['umb'] = os.path.getsize(os.path.join(NOS, 'um.py'))
    if str((selo.get('sha256') or {}).get('um.py', '')) != V['s64']:
        P.append('selo.sha256(um.py) != disco')
    if not (ap['um_py_novo']['sha16'] == V['s16'] == ESP['candidato_sha16'] == CM['sha16']):
        P.append('um.py do disco (%s) != instalado/esperado/candidato' % V['s16'])
    V['base16'] = ap['backups']['um.py']['sha16']
    if V['base16'] != ESP['origem_sha16']:
        P.append('a base substituida (%s) != a v386 selada (%s)' % (V['base16'], ESP['origem_sha16']))
    V['n_patches'] = len(CM['patches']); V['patches'] = ', '.join(p['id'] for p in CM['patches'])
    V['instalado_em'] = '%s-%s-%s %s:%s:%s' % (ap['ts'][0:4], ap['ts'][4:6], ap['ts'][6:8], ap['ts'][9:11], ap['ts'][11:13], ap['ts'][13:15])
    m = re.search(r'teoremas limpos:\s*(\d+)/(\d+)', out)
    V['teor'] = '%s/%s' % m.groups() if m else 'AUSENTE'
    if not m or m.group(1) != m.group(2) or [int(m.group(1)), int(m.group(2))] != ESP['escada']:
        P.append('teoremas limpos ausente, N != M ou != a escada esperada (%s)' % V['teor'])
    if 'FAIL_CLOSED_SELFTEST_PASSED' not in out or selo.get('fail_closed_selftest') != 'FAIL_CLOSED_SELFTEST_PASSED':
        P.append('selftest nao PASSED (stdout ou selo)')
    if '>>> TGL_KERNEL_FORMALIZATION_FAILED <<<' in out or '>>> TGL_KERNEL_STAGE1_VERIFIED' not in out:
        P.append('a verificacao principal do kernel nao leu VERIFIED')
    if 'SEAL_WITHHELD' in out:
        P.append('o stdout traz SEAL_WITHHELD')
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
    mrc = re.findall(r'^RITO_RC=(\S+)', out, flags=re.M)
    V['rc'] = mrc[-1] if mrc else 'NAO_LIDO'
    if V['rc'] != '0':
        P.append('rc do rito nao lido como 0 (%s)' % V['rc'])
    V['v387_linhas'] = [l.strip() for l in out.splitlines() if '[v387]' in l]
    if len(V['v387_linhas']) != 4:
        P.append('o stdout nao tem as 4 linhas [v387] (%d)' % len(V['v387_linhas']))
    hp = os.path.join(PK, 'rito_horarios_v387.txt')
    V['horarios'] = open(hp, encoding='utf-8').read().split() if os.path.exists(hp) else []
    # o selo e o gate
    V['selo_ts'] = selo.get('timestamp'); V['um_version'] = selo.get('um_version'); V['qg'] = selo.get('qg_closure_verdict')
    if V['um_version'] != 'v387':
        P.append('o selo nao e v387 (%s)' % V['um_version'])
    if V['qg'] != ESP['qg_closure_verdict_v386']:
        P.append('o gate MUDOU')
    qg = core.get('qg_closure') or {}
    V['n18'] = sum(1 for fam in ('formal_flags', 'physics_flags', 'experiment_flags') for v in (qg.get(fam) or {}).values() if v is True)
    if V['n18'] != 18:
        P.append('as bandeiras do gate nao sao 18 (%s)' % V['n18'])
    V['beta'] = core.get('beta')
    for k in ('um_absoluto.json', 'um_absoluto_selo.json', 'um_absoluto_forma_canonica.md', 'um_absoluto_manifest.md'):
        V['h_' + k] = sha(os.path.join(NOS, k))[:16] if os.path.exists(os.path.join(NOS, k)) else 'AUSENTE'
    V['artigos'] = {os.path.basename(p): sha(p)[:16] for p in sorted(glob.glob(os.path.join(NOS, 'um_absoluto_??.pdf')) + glob.glob(os.path.join(NOS, 'um_absoluto_??.txt')))}
    # o conferidor (a copia congelada que a cadeia rodou)
    cp = os.path.join(HERE, 'conferidor', 'conferencia_rito_v387.json')
    if os.path.exists(cp):
        C = json.load(open(cp, encoding='utf-8'))
        V['conf16'] = sha(cp)[:16]; V['conf_tudo'] = C.get('tudo_bate') is True
        V['conf_dm'] = '%d/%d' % (sum(1 for v in C['deve_mudar'].values() if v), len(C['deve_mudar']))
        V['conf_np'] = '%d/%d' % (sum(1 for v in C['nao_pode_mudar'].values() if v), len(C['nao_pode_mudar']))
        V['n_ver_mudaram'] = len(C.get('vereditos_que_mudaram') or {}); V['servidor'] = C.get('servidor_depois_do_rito')
        if not V['conf_tudo']:
            P.append('o conferidor NAO bateu')
    else:
        V['conf16'] = 'AUSENTE'; V['conf_tudo'] = False; P.append('a conferencia do rito nao foi achada em v387_selo/conferidor')
    V['n_ver'] = len(ESP['vereditos_v386'])
    # os quatro registros
    for k in REG:
        r = core.get(k) or {}
        V[k] = r.get('verdict'); V[k + '_ok'] = r.get('all_verified') is True
        if not V[k + '_ok']:
            P.append('%s nao selou (%s)' % (k, str(r.get('verdict'))[:120]))
        if GUARDA.search(str(r.get('verdict') or '')):
            P.append('%s com palavra proibida' % k)
        if (selo.get(k) or {}).get('verdict') != r.get('verdict'):
            P.append('o selo nao registra o mesmo veredito de %s' % k)
    tt = core.get('three_stress_tests_v387') or {}
    V['tt'] = {k: tt.get(k) for k in ('n_verdicts', 'n_not_falsified', 'n_inconclusive', 'n_awaiting', 'falsified_substring_paths', 'n_forbidden_word_as_verdict')}
    V['tt_kernel'] = tt.get('kernel'); V['tt_gpu'] = tt.get('gpu'); V['tt_ledger'] = tt.get('ledger'); V['tt_joint'] = tt.get('joint'); V['tt_echo'] = tt.get('echo_routes_outside_the_ledger')
    hr = core.get('hubble_ratio_v387') or {}; pr = core.get('primordial_v387') or {}
    V['hr_tr'] = hr.get('transcribed') or {}; V['pr_tr'] = pr.get('transcribed') or {}
    V['hr_beta_rel'] = (hr.get('beta') or {}).get('rel_diff'); V['pr_beta_rel'] = (pr.get('beta') or {}).get('rel_diff')
    V['V1'] = {n: {'id': P_['identificador'], 'spec16': P_['spec_sha256'][:16], 'funcao16': P_['funcao_sha256'][:16], 'json16': P_['files']['json']['sha256'][:16],
                   'pasta': P_['files']['json']['path'].rsplit('\\', 1)[0]} for n, P_ in ESP['V1'].items()}
    V['verbatins'] = ESP['verbatins']
    qp = core.get('quantum_pillar_v384') or {}
    V['pilar'] = {'mode': qp.get('mode'), 'result16': str(qp.get('result_sha256'))[:16], 'key': qp.get('key')}
    V['retro_sites'] = [s_['id'] for s_ in CM['retro_sites']]
    import datetime
    V['data'] = datetime.datetime.now().strftime('%d/%m/%Y'); V['hora'] = datetime.datetime.now().strftime('%H:%M')
    return V, P


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    V, P = ler()
    print(json.dumps({k: v for k, v in V.items() if k not in ('v387_linhas',)}, ensure_ascii=False, indent=1, default=str)[:6000])
    print('PROBLEMAS:', P if P else 'nenhum')
    sys.exit(1 if P else 0)
