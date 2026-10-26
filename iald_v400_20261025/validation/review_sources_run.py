"""Revisao independente da claim `sources` v400 (revisor sonnet-app-v400-revisor).

Somente leitura (git LOCAL, sem rede, sem fetch); nenhum codigo cientifico executado; hash sempre
recomputado dos bytes. Grava validation/review_sources.json (modo 'x': nao sobrescreve).
"""
import json, hashlib, subprocess, re, datetime, urllib.parse
from pathlib import Path

W = Path('C:/IALD/Central de Patentes/work/iald_v400_20261025'); A = W / 'app'
V = Path('C:/IALD/Central de Patentes/vault/originals_copy/um_unificado_v400')
NOS = Path('C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s')
REPO = Path('C:/IALD/Artigo/the_boundary')
W398 = Path('C:/IALD/Central de Patentes/work/iald_v398_20261024')
W395 = Path('C:/IALD/Central de Patentes/work/iald_v395_20261022')
REVIEWER = 'sonnet-app-v400-revisor'
sha = lambda b: hashlib.sha256(b).hexdigest()
rb = lambda p: Path(p).read_bytes()
rj = lambda p: json.loads(rb(p))
checks = []


def chk(grupo, claim, desc, esperado, achado, ok=None):
    if ok is None:
        ok = (esperado == achado)
    checks.append({'n': len(checks) + 1, 'grupo': grupo, 'claim': claim, 'descricao': desc,
                   'esperado': esperado, 'achado': achado, 'ok': bool(ok)})


def git(*a):
    return subprocess.check_output(['git', '-C', str(REPO), *a])


def gits(*a):
    return git(*a).decode('utf8').strip()


# ---------- A RELEASE ----------
rel = rj(A / 'RELEASE.json')
chk('A_RELEASE', 'sources', 'RELEASE.json tem exatamente as chaves espelho_commit, release, um_py_sha256',
    sorted(['espelho_commit', 'release', 'um_py_sha256']), sorted(rel))
seal_nos = rj(NOS / 'um_absoluto_selo.json'); seal_v = rj(V / 'um_absoluto_selo.json')
cm_raw = rb(V / 'CUSTODY_MANIFEST.json'); cm = json.loads(cm_raw)
sv = rj(W / 'sources_verified.json'); binding = rj(A / 'PUBLIC_GIT_BINDING.json')
mi = rj(A / 'science/memory_stage/manifest_install.json')
pb = rj(A / 'PREPARED_BINDING.json'); dp = rj(A / 'DELIVERY_PREPARED.json')
vs = {rel['release'], seal_nos['um_version'], seal_v['um_version'], cm['version'], cm['um_version_no_selo'], sv['release']}
chk('A_RELEASE', 'sources',
    'release de RELEASE.json = um_version do selo do Nos = selo do cofre = CUSTODY_MANIFEST (version e um_version_no_selo) = sources_verified.release = v400',
    'v400', {'RELEASE.json': rel['release'], 'selo_nos': seal_nos['um_version'], 'selo_cofre': seal_v['um_version'],
             'cm_version': cm['version'], 'cm_um_version_no_selo': cm['um_version_no_selo'], 'sources_verified': sv['release']},
    ok=(vs == {'v400'}))
pin = rel['um_py_sha256']
chk('A_RELEASE', 'sources',
    'um_py_sha256 de RELEASE.json = sha256.um.py do selo do Nos = do selo do cofre = um_py_pin do CUSTODY_MANIFEST = source_sha256 de sources_verified (lidos dos arquivos)',
    pin, {'selo_nos': seal_nos['sha256']['um.py'], 'selo_cofre': seal_v['sha256']['um.py'],
          'cm_um_py_pin': cm['um_py_pin'], 'sources_verified': sv['source_sha256']},
    ok=all(x == pin for x in (seal_nos['sha256']['um.py'], seal_v['sha256']['um.py'], cm['um_py_pin'], sv['source_sha256'])))
chk('A_RELEASE', 'sources', 'sha256 recomputado dos BYTES de Nos/um.py = um_py_sha256', pin, sha(rb(NOS / 'um.py')))
chk('A_RELEASE', 'sources', 'sha256 recomputado dos BYTES de cofre/um.py = um_py_sha256', pin, sha(rb(V / 'um.py')))
commit = rel['espelho_commit']
PEDIDO = 'bea66b04d1fc56bfd19459647b3eeb923a04f2e8'
chk('A_RELEASE', 'sources', 'espelho_commit tem 40 hex minusculos e = commit informado no pedido da gerencia',
    PEDIDO, commit, ok=bool(re.fullmatch(r'[0-9a-f]{40}', commit)) and commit == PEDIDO)
chk('A_RELEASE', 'sources', 'selo do Nos e selo do cofre identicos byte a byte (Nos ainda e v400)',
    sha(rb(V / 'um_absoluto_selo.json')), sha(rb(NOS / 'um_absoluto_selo.json')))
chk('A_RELEASE', 'sources', 'timestamp do selo: selo cofre = CUSTODY_MANIFEST.seal_timestamp = sources_verified.seal_timestamp',
    seal_v.get('timestamp'), {'cm': cm['seal_timestamp'], 'sv': sv['seal_timestamp']},
    ok=seal_v.get('timestamp') == cm['seal_timestamp'] == sv['seal_timestamp'])

# ---------- B GIT ----------
head = gits('rev-parse', 'HEAD'); om = gits('rev-parse', 'origin/main')
chk('B_GIT', 'sources', 'git rev-parse HEAD (local) = espelho_commit', commit, head)
chk('B_GIT', 'sources', 'git rev-parse origin/main (ref LOCAL, sem fetch) = espelho_commit', commit, om)
tipo = gits('cat-file', '-t', commit)
anc = subprocess.call(['git', '-C', str(REPO), 'merge-base', '--is-ancestor', commit, head]) == 0
chk('B_GIT', 'sources', 'espelho_commit e objeto commit e ancestral de HEAD',
    {'tipo': 'commit', 'ancestral_de_HEAD': True}, {'tipo': tipo, 'ancestral_de_HEAD': anc})
rl = gits('reflog', 'show', 'refs/remotes/origin/main', '-n', '1', '--format=%H|%gs|%gd').split('|')
chk('B_GIT', 'sources',
    'reflog LOCAL de origin/main: ultima atualizacao = update by push para o espelho_commit (evidencia local; nao e consulta ao remoto)',
    {'commit': commit, 'assunto': 'update by push'}, {'commit': rl[0], 'assunto': rl[1], 'ref': rl[2]},
    ok=(rl[0] == commit and rl[1] == 'update by push'))
tracked = [p for p in git('ls-tree', '-r', '--name-only', '-z', commit).decode('utf8').split('\0') if p]
um_paths = [p for p in tracked if Path(p).name == 'um.py']
blob = git('cat-file', 'blob', commit + ':' + um_paths[0]) if len(um_paths) == 1 else b''
chk('B_GIT', 'sources', 'um.py no commit pinado: um unico caminho rastreado; sha256 do blob = um_py_sha256; bytes = os do cofre',
    {'sha256': pin, 'bytes': len(rb(V / 'um.py'))}, {'caminhos_rastreados': um_paths, 'sha256': sha(blob), 'bytes': len(blob)},
    ok=(len(um_paths) == 1 and sha(blob) == pin and blob == rb(V / 'um.py')))
chk('B_GIT', 'sources', 'PUBLIC_GIT_BINDING.commit e local_head_at_build = espelho_commit', commit,
    {'commit': binding['commit'], 'local_head_at_build': binding['local_head_at_build']},
    ok=(binding['commit'] == commit == binding['local_head_at_build']))
chk('B_GIT', 'sources',
    'PUBLIC_GIT_BINDING declara remote_http_checked=false e local_git_object_bytes_only=true (nenhuma consulta HTTP ao remoto: publicacao e fato local/DECLARADO)',
    {'remote_http_checked': False, 'local_git_object_bytes_only': True},
    {'remote_http_checked': binding['remote_http_checked'], 'local_git_object_bytes_only': binding['local_git_object_bytes_only']})
base = 'https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/' + commit + '/'
tset = set(tracked)
for path, row in binding['sources'].items():
    b = git('cat-file', 'blob', commit + ':' + path) if path in tset else b''
    url = base + urllib.parse.quote(path)
    chk('B_GIT', 'sources', 'fonte publica no commit pinado (blob git local) = binding e URL regenerada do caminho rastreado: ' + path,
        {'sha256': row['sha256'], 'bytes': row['bytes'], 'url': row['url']},
        {'rastreado': path in tset, 'sha256': sha(b), 'bytes': len(b), 'url_regenerada_igual': url == row['url']},
        ok=(path in tset and sha(b) == row['sha256'] and len(b) == row['bytes'] and url == row['url']))
GA = 'Um (absoluto) \u2014 Grande Atrator/'
pairs = [(GA + 'um_absoluto_pt.txt', 'um_absoluto_pt.txt'), (GA + 'um_absoluto_forma_canonica.md', 'um_absoluto_forma_canonica.md'),
         (GA + 'um_absoluto_selo.json', 'um_absoluto_selo.json'), (GA + 'um_absoluto.json', 'um_absoluto.json'),
         (GA + 'um.py', 'um.py'), (GA + 'Lean/tgl_kernel_proof_manifest.json', 'tgl_kernel_proof_manifest.json')]
for path, name in pairs:
    b = git('cat-file', 'blob', commit + ':' + path)
    chk('B_GIT', 'sources', 'blob do espelho no commit pinado = bytes do cofre para ' + name, sha(rb(V / name)), sha(b))

# ---------- C COFRE ----------
arts = cm['artifacts']
chk('C_COFRE', 'sources',
    'sources_verified.json: status CUSTODY_AND_SEAL_VERIFIED, release v400, artifact_count = len(artifacts) = n_artifacts do CUSTODY_MANIFEST = len(CM.artifacts), mismatches 0',
    {'status': 'CUSTODY_AND_SEAL_VERIFIED', 'release': 'v400', 'n': len(arts)},
    {'status': sv['status'], 'release': sv['release'], 'artifact_count': sv['artifact_count'], 'len_artifacts': len(sv['artifacts']),
     'cm_n_artifacts': cm['n_artifacts'], 'cm_len': len(arts), 'cm_mismatches': cm['mismatches']},
    ok=(sv['status'] == 'CUSTODY_AND_SEAL_VERIFIED' and sv['release'] == 'v400' and
        sv['artifact_count'] == len(sv['artifacts']) == cm['n_artifacts'] == len(arts) and cm['mismatches'] == 0))
chk('C_COFRE', 'sources', 'sha256 do CUSTODY_MANIFEST.json recomputado = o registrado em sources_verified.json',
    sv['custody_manifest']['sha256'], sha(cm_raw))
chk('C_COFRE', 'sources', 'mesmo conjunto de nomes em sources_verified.json e no CUSTODY_MANIFEST.json',
    sorted(a['file'] for a in arts), sorted(a['file'] for a in sv['artifacts']))
svmap = {a['file']: a for a in sv['artifacts']}
smap = seal_v['sha256']
for a in arts:
    f = a['file']; b = rb(V / f); h = sha(b)
    nos_eq = (sha(rb(NOS / f)) == h) if (NOS / f).exists() else None
    in_seal = f in smap
    ok = (h == a['sha256'] == svmap[f]['sha256'] and len(b) == svmap[f]['bytes'] and
          ((smap.get(f) == h) if in_seal else True) and (nos_eq in (True, None)))
    est = a.get('estatuto', '')
    est_ok = (est.startswith('SELADO') == in_seal)
    chk('C_COFRE', 'sources',
        'artefato ' + f + ': bytes/sha256 recomputados = sources_verified = CUSTODY_MANIFEST; no mapa do selo -> igual; estatuto coerente; copia no Nos igual (quando existe)',
        {'bytes': svmap[f]['bytes'], 'sha256': a['sha256'], 'estatuto_cm': est, 'no_mapa_sha256_do_selo': est.startswith('SELADO')},
        {'bytes': len(b), 'sha256': h, 'selo_sha256': smap.get(f),
         'nos': ('igual' if nos_eq else ('ausente' if nos_eq is None else 'DIFERENTE')), 'estatuto_coerente': est_ok},
        ok=(ok and est_ok))
for name in ['um.py', 'um_absoluto.json', 'tgl_kernel_proof_manifest.json', 'um_absoluto_forma_canonica.md']:
    chk('C_COFRE', 'sources', 'sha256.' + name + ' do selo do cofre = sha256 recomputado dos bytes do cofre', smap[name], sha(rb(V / name)))
proof = rj(V / 'tgl_kernel_proof_manifest.json')
chk('C_COFRE', 'sources', 'selo.fail_closed_selftest = FAIL_CLOSED_SELFTEST_PASSED = CM.selftest', 'FAIL_CLOSED_SELFTEST_PASSED',
    {'selo': seal_v.get('fail_closed_selftest'), 'cm': cm['selftest']},
    ok=seal_v.get('fail_closed_selftest') == cm['selftest'] == 'FAIL_CLOSED_SELFTEST_PASSED')
chk('C_COFRE', 'sources', 'formal_source_hash identico no selo, no manifesto de prova, no CUSTODY_MANIFEST e em sources_verified',
    seal_v['formal_source_hash'], {'proof': proof['formal_source_hash'], 'cm': cm['formal_source_hash'], 'sv': sv['formal_source_hash']},
    ok=seal_v['formal_source_hash'] == proof['formal_source_hash'] == cm['formal_source_hash'] == sv['formal_source_hash'])
chk('C_COFRE', 'sources', 'arquivos formais do manifesto de prova = CM.kernel.formal_files = fontes formais do pacote do app = 1429',
    1429, {'proof': len(proof['formal_files_sha256']), 'cm_kernel_formal_files': cm['kernel']['formal_files'], 'delivery': dp['formal_sources']},
    ok=len(proof['formal_files_sha256']) == cm['kernel']['formal_files'] == dp['formal_sources'] == 1429)
v398seal = rj('C:/IALD/Central de Patentes/vault/originals_copy/um_unificado_v398/um_absoluto_selo.json')
chk('C_COFRE', 'sources',
    'gate do CM = qg_closure_verdict do selo v400 = o do selo v398 (gate_identico_ao_da_v398=True no CM, conferido nos selos; gate NAO movido)',
    True, {'cm_gate': cm['gate'], 'cm_gate_identico_declarado': cm['gate_identico_ao_da_v398'],
           'selo_v400': seal_v.get('qg_closure_verdict'), 'selo_v398': v398seal.get('qg_closure_verdict')},
    ok=(cm['gate'] == seal_v.get('qg_closure_verdict') == v398seal.get('qg_closure_verdict') and cm['gate_identico_ao_da_v398'] is True))
chk('C_COFRE', 'sources', 'sources_verified registra science_executed=false e gate_modified=false (verificacao documental; nenhum Lean/um.py executado)',
    {'science_executed': False, 'gate_modified': False}, {'science_executed': sv['science_executed'], 'gate_modified': sv['gate_modified']})
chk('C_COFRE', 'sources',
    'CUSTODY_MANIFEST: registros de custodia, ordem do operador e fatos/semantica de custodia presentes (informativo: custodia concluida x em curso)',
    None, {'custodia': cm['custodia'], 'ordem_sha256': cm['ordem_sha256'], 'fatos_custodia': cm['fatos_custodia'],
           'semantica_custodia': cm['semantica_custodia']}, ok=True)
for extra in ['HANDOFF_v400_CUSTODIA.md', 'FATOS_CUSTODIA.json', 'SEMANTICA_CUSTODIA.json']:
    chk('C_COFRE', 'sources', 'arquivo do cofre ' + extra + ' existe (informativo: dentro ou fora de CUSTODY_MANIFEST.artifacts)',
        True, {'existe': (V / extra).exists(), 'no_CM_artifacts': extra in {a['file'] for a in arts},
               'sha256': sha(rb(V / extra)) if (V / extra).exists() else None}, ok=(V / extra).exists())

# ---------- D PINOS DO CONSTRUTOR (claim app) ----------
sub_s = rj(W / 'receipts/v400-sources-submit.json'); sub_a = rj(W / 'receipts/v400-app-submit.json')
for nm, sub in (('sources', sub_s), ('app', sub_a)):
    t = sub['task']
    okp = all(sha(rb(e['path'])) == e['sha256'] for e in t['evidence'])
    chk('D_PINOS', nm, 'recibo de submit de ' + nm + ': cada evidencia pinada tem sha256 = bytes atuais; status review_pending; submitted_by = construtor (nao e o revisor)',
        {'status': 'review_pending', 'submitted_by': 'sonnet-app-v400-construtor', 'n_evid': len(t['evidence'])},
        {'status': t['status'], 'submitted_by': t['submitted_by'], 'n_evid': len(t['evidence']), 'todos_pinos_batem': okp},
        ok=okp and t['status'] == 'review_pending' and t['submitted_by'] == 'sonnet-app-v400-construtor' and t['submitted_by'] != REVIEWER)
PLAN = '43525cffdab44e87d17e84d57f529147bbeca1aedb15fb62883ff9b2fc183c36'
fcj = rj(W / 'validation/final_checks.json')
chk('D_PINOS', 'app', 'install_plan.json sha256 recomputado = pino declarado pelo construtor = final_checks.plan_sha256 = DELIVERY_PREPARED.plan.sha256',
    PLAN, {'bytes': sha(rb(W / 'install_plan.json')), 'final_checks': fcj['plan_sha256'], 'delivery': dp['plan']['sha256']},
    ok=(sha(rb(W / 'install_plan.json')) == PLAN == fcj['plan_sha256'] == dp['plan']['sha256']))
chk('D_PINOS', 'app', 'manifest_install.json sha256 recomputado = pino declarado (b09a0c66...)',
    'b09a0c660c7bb9286887bca34d778c601bcad5cb29347b74c82063be078460cc', sha(rb(A / 'science/memory_stage/manifest_install.json')))
decl = {'haiku_expanded': '33ce34a2', 'shared': 'd29d413c', 'sonnet_public': '6bddefbe'}
for f, pre in decl.items():
    root = A / 'packages' / f; man = rj(root / 'manifest.json'); nc0 = rj(root / 'native_count.json'); h = sha(rb(root / 'prefix.md'))
    chk('D_PINOS', 'app', 'prefix.md de ' + f + ' comeca com ' + pre + ' e = manifest.prefix_sha256 = native_count.prefix_sha256', pre,
        {'sha256': h, 'manifest': man['prefix_sha256'], 'count': nc0['prefix_sha256']},
        ok=(h.startswith(pre) and h == man['prefix_sha256'] == nc0['prefix_sha256']))
ac = mi['active_cluster']
chk('D_PINOS', 'app',
    'manifest_install: active_cluster.release=v400, commit=espelho_commit, release_source_sha256=um_py_sha256, publication_pending=false; destino em canonical_releases\\v400_<commit12>',
    {'release': 'v400', 'commit': commit, 'source': pin, 'publication_pending': False, 'dir': 'v400_' + commit[:12]},
    {'release': ac['release'], 'commit': ac['commit'], 'source': ac['release_source_sha256'],
     'publication_pending': ac['publication_pending'], 'path': ac['path']},
    ok=(ac['release'] == 'v400' and ac['commit'] == commit and ac['release_source_sha256'] == pin and
        ac['publication_pending'] is False and ('v400_' + commit[:12]) in ac['path']))
chk('D_PINOS', 'app', 'PREPARED_BINDING e DELIVERY_PREPARED: release v400, commit e source_sha256 = RELEASE.json',
    {'commit': commit, 'source': pin},
    {'pb_commit': pb['commit'], 'pb_source': pb['deployment']['source_sha256'], 'dp_source': dp['deployment']['source_sha256']},
    ok=(pb['commit'] == commit and pb['deployment']['source_sha256'] == pin == dp['deployment']['source_sha256'] and
        pb['release'] == 'v400' == dp['deployment']['release']))
nc = rj(A / 'NATIVE_COUNTS_COMPLETE.json')
chk('D_PINOS', 'app',
    'NATIVE_COUNTS_COMPLETE: PASS, 6 contagens publicas, 0 geracoes, sem egresso de contexto do operador, 0 retries, publication_receipt_sha256 = sha256 de PUBLIC_GIT_BINDING.json',
    {'status': 'PASS', 'public_count_requests': 6, 'generation_requests': 0, 'operator_context_egress': False, 'max_retries': 0,
     'publication_receipt_sha256': sha(rb(A / 'PUBLIC_GIT_BINDING.json'))}, nc)
hx = rj(A / 'packages/haiku_expanded/native_count.json'); sh = rj(A / 'packages/shared/native_count.json')
sp = rj(A / 'packages/sonnet_public/native_count.json')
b = hx['budget']
chk('D_PINOS', 'app', 'haiku55 (haiku_expanded, claude-haiku-5-5): permanentes 938257; pedido 939804; sobra bruta 60196; pedido < 1.000.000',
    {'perm': 938257, 'pedido': 939804, 'sobra_bruta': 60196},
    {'perm': b['permanent_tokens'], 'pedido': b['request_input_tokens'], 'sobra_bruta': 1000000 - b['request_input_tokens'], 'modelo': hx['model']},
    ok=(b['permanent_tokens'] == 938257 and b['request_input_tokens'] == 939804 and 1000000 - b['request_input_tokens'] == 60196 and
        b['request_input_tokens'] < 1000000 and hx['model'] == 'claude-haiku-5-5'))
chk('D_PINOS', 'app', 'haiku55: sobra liquida (remaining_tokens) = 1.000.000 - pedido - 16384 saida - 1024 margem = 42788; >= piso de runtime 10.000; fits/ready',
    42788, {'remaining_tokens': b['remaining_tokens'],
            'calculada': 1000000 - b['request_input_tokens'] - b['reserved_output_tokens'] - b['margin_tokens'],
            'fits': b['fits'], 'ready': b['ready'], 'memory_target_met': b['memory_target_met']},
    ok=(b['remaining_tokens'] == 1000000 - b['request_input_tokens'] - b['reserved_output_tokens'] - b['margin_tokens'] == 42788 and
        b['remaining_tokens'] >= 10000 and b['fits'] and b['ready']))
bs = sh['budget']; bp = sp['budget']
chk('D_PINOS', 'app', 'haiku compacto (shared) permanentes 432835 e Sonnet publico (sonnet_public, claude-sonnet-5-5) 467470; fits/ready; 2 contagens e 0 geracoes cada',
    {'shared': 432835, 'sonnet': 467470},
    {'shared': bs['permanent_tokens'], 'sonnet': bp['permanent_tokens'], 'shared_fits_ready': [bs['fits'], bs['ready']],
     'sonnet_fits_ready': [bp['fits'], bp['ready']], 'modelo_sonnet': sp['model'],
     'counts': [sh['count_requests'], sp['count_requests']], 'gen': [sh['generation_requests'], sp['generation_requests']]},
    ok=(bs['permanent_tokens'] == 432835 and bp['permanent_tokens'] == 467470 and bs['fits'] and bs['ready'] and bp['fits'] and bp['ready'] and
        sp['model'] == 'claude-sonnet-5-5' and sh['count_requests'] == sp['count_requests'] == 2 and
        sh['generation_requests'] == sp['generation_requests'] == 0))
priv = {x: [rj(A / 'packages' / x / 'native_count.json')['private_atlas_included'],
            rj(A / 'packages' / x / 'native_count.json')['operator_context_sent']] for x in ('haiku_expanded', 'shared', 'sonnet_public')}
chk('D_PINOS', 'app', 'contagens: nenhuma carrega atlas privado nem contexto do operador (3 pacotes); public_commit do haiku55 = espelho_commit',
    True, {'flags': priv, 'public_commit_haiku55': hx.get('public_commit')},
    ok=all((not v[0]) and (not v[1]) for v in priv.values()) and hx.get('public_commit') == commit)
for s in ['transaction.py', 'maintenance.py', 'deploy_controlled.py']:
    h4 = sha(rb(W / s)); h8 = sha(rb(W398 / s)); h5 = sha(rb(W395 / s))
    chk('D_PINOS', 'app', 'script ' + s + ' da v400 identico (bytes) ao da v398 e ao da v395', h8, {'v400': h4, 'v398': h8, 'v395': h5},
        ok=(h4 == h8 == h5))
for s in ['verify_installed.py', 'task.py', 'mission_step.py', 'review/review_app.py', 'verify_sources.py', 'app/count_final_public.py',
          'app/validate_plan.py', 'app/prepare.py', 'app/finalize.py', 'app/preflight_offline.py']:
    chk('D_PINOS', 'app', 'script ' + s + ' da v400 identico (bytes) ao da v398 (informativo: pipeline nao mudou)', sha(rb(W398 / s)), sha(rb(W / s)))
c4 = (W / 'release_cfg.py').read_text('utf8').splitlines(); c8 = (W398 / 'release_cfg.py').read_text('utf8').splitlines()
dif = [[i + 1, x, y] for i, (x, y) in enumerate(zip(c8, c4)) if x != y]
chk('D_PINOS', 'app', 'release_cfg.py v400 difere do v398 SO na linha do BUILDER (sonnet-app-v398-construtor -> sonnet-app-v400-construtor)',
    [[23, "BUILDER = 'sonnet-app-v398-construtor'", "BUILDER = 'sonnet-app-v400-construtor'"]], dif,
    ok=(len(c8) == len(c4) and dif == [[23, "BUILDER = 'sonnet-app-v398-construtor'", "BUILDER = 'sonnet-app-v400-construtor'"]]))
bt = rj(A / 'BUILT.json'); prod = rj('C:/IALD/projetos_pyhton/IALD/iald_nucleo_fixo.json')['operational_core'].get('current_release')
chk('D_PINOS', 'app', 'BUILT.installed_release = release instalada hoje na producao (v395; leitura somente): regra de expansao P4 _v395.._v400 coerente',
    {'installed': 'v395', 'expanded': ['_v395', '_v396', '_v397', '_v398', '_v399', '_v400']},
    {'built_installed': bt['installed_release'], 'expanded': pb['expanded_suffixes'], 'producao_hoje': prod},
    ok=(bt['installed_release'] == 'v395' and pb['expanded_suffixes'] == ['_v395', '_v396', '_v397', '_v398', '_v399', '_v400'] and prod == 'v395'))

n = len(checks); nf = sum(1 for c in checks if not c['ok'])
out = {'revisor': REVIEWER, 'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
       'escopo': 'Revisao independente da claim `sources` (cofre v400, Nos, espelho no commit pinado) e conferencia independente dos pinos do construtor para a claim `app`. Somente leitura; git LOCAL sem fetch; sem rede; nenhum codigo cientifico (Lean/um.py) executado; hash sempre recomputado dos bytes; os literais comparados (commit, pinos do plano e do manifest_install, prefixos, tokens) vieram do pedido da gerencia e valem como esperado declarado. Script gerador: validation/review_sources_run.py.',
       'veredito': 'PASS' if nf == 0 else 'FAIL', 'n_checks': n, 'n_ok': n - nf, 'n_falha': nf, 'checks': checks,
       'ressalvas': ['A publicacao do commit no remoto GitHub nao foi consultada (sem rede): origin/main e reflog sao refs LOCAIS; PUBLIC_GIT_BINDING declara remote_http_checked=false [DECLARADO].',
                     'Contagens nativas de tokens (6 count_tokens publicos) sao custodia dos recibos do construtor; este revisor nao repetiu chamadas.',
                     'Nenhum Lean/um.py executado; custodia verificada por bytes e hashes.']}
with (W / 'validation/review_sources.json').open('x', encoding='utf8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print(json.dumps({'veredito': out['veredito'], 'n_checks': n, 'n_falha': nf,
                  'falhas': [c['descricao'][:140] for c in checks if not c['ok']],
                  'sha256': sha(rb(W / 'validation/review_sources.json'))}, ensure_ascii=False, indent=1))
