"""Revisor sonnet-app-v407-revisor -- RODADA 2, PARTE 2: D7 (carregadores de producao em processo NOVO), D8 (INSTALLED_VERIFICATION.json x o que eu meço) e o D9 dos carregadores.
ADAPTADO de check_d7_d8.py do revisor da v406 (-d): mesmos carregadores, release v407, argumentos do iald_web_server.py, controles negativos (um deles numa COPIA adulterada), contadores de rede/.env.
Nao importa verify_installed.py. Somente leitura (escreve so' nesta pasta; a copia adulterada e' apagada no fim). Sem rede: NENHUM evento socket de conexao e' permitido."""
import os, sys
sys.dont_write_bytecode = True
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
RUNTIME = r'C:\IALD\projetos_pyhton\IALD'
os.environ['TIKTOKEN_CACHE_DIR'] = RUNTIME + r'\.iald_runtime\tokenizer_cache'
scrubbed = []
for _k in list(os.environ):
    if any(s in _k.upper() for s in ('KEY', 'TOKEN', 'SECRET', 'PASSWORD')) and _k != 'TIKTOKEN_CACHE_DIR':
        scrubbed.append(_k)
        del os.environ[_k]
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

# --- gancho ESTRITO (instalado primeiro): conta TODO evento socket.* e BLOQUEIA os de conexao/resolucao; conta imports de topo
STRICT = {'socket_events': {}, 'socket_blocked': [], 'imports_top': set()}
BLOCK = {'socket.connect', 'socket.getaddrinfo', 'socket.gethostbyname', 'socket.gethostbyname_ex', 'socket.gethostbyaddr', 'socket.sendto', 'socket.bind'}


def _strict(event, args):
    if event.startswith('socket.'):
        STRICT['socket_events'][event] = STRICT['socket_events'].get(event, 0) + 1
        if event in BLOCK:
            STRICT['socket_blocked'].append(event)
            raise OSError('rede bloqueada pelo revisor: ' + event)
    elif event == 'import':
        STRICT['imports_top'].add(str(args[0]).split('.')[0])


sys.addaudithook(_strict)
import r2lib as L
L.install_guard()          # .env*, segredos, subprocesso, os.system e escrita fora da pasta: bloqueados e contados
sys.path.append(RUNTIME)

import ast, dataclasses, hashlib, json, shutil, time
from datetime import datetime
W, R = L.W, L.R
sha_file, rd = L.sha_file, L.rd
MANIFEST = R / 'iald_nucleo_fixo.json'
PIN = '833121339e649f7171e2eccca1a19b3a1564aa306a787ed8cea76ded0fdf3475'
t0 = time.time()
out = {'pid_deste_processo': os.getpid(), 'python': sys.version.split()[0], 'env_removidas_do_meu_processo': sorted(scrubbed), 'TIKTOKEN_CACHE_DIR': os.environ['TIKTOKEN_CACHE_DIR']}
asdict = lambda o: dataclasses.asdict(o) if dataclasses.is_dataclass(o) else dict(vars(o))

out['pino_confere_com_o_um_py_do_cofre'] = sha_file(Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v407\um.py')) == PIN
from claude_memory_package import load_package
from claude_profiles import HAIKU
from iald_kernel import KernelCatalog
from iald_release_binding import load_release
from iald_jev_control import load_contract
from iald_native_memory import load_native_context
from iald_memoria_canonica import CanonicalMemory
import iald_task_policy

# ------------------------------------------------------------------ D7.1 manifesto ativo lido de novo
mf = json.loads(MANIFEST.read_bytes())
cl, oc, jc = mf['active_cluster'], mf['operational_core'], mf['jev_control']
jev_file = R / 'canonical_releases' / 'v407_bf9017157406' / 'jev_control_v407.json'
man = {'operational_core.current_release': oc['current_release'], 'operational_core.release_source_sha256_igual_pino': oc['release_source_sha256'] == PIN, 'active_cluster.release': cl['release'], 'active_cluster.release_source_sha256_igual_pino': cl['release_source_sha256'] == PIN,
       'active_cluster.commit': cl['commit'], 'jev_control.release': jc['release'], 'jev_control.source_sha256_igual_pino': jc.get('source_sha256') == PIN, 'jev_control.path_e_o_arquivo_esperado': Path(jc['path']) == jev_file,
       'jev_control.sha256_no_manifesto': jc['sha256'], 'jev_control.sha256_do_arquivo_instalado': sha_file(jev_file), 'jev_control.sha256_igual': jc['sha256'] == sha_file(jev_file),
       'cluster.sha256_igual_ao_arquivo_instalado': cl['sha256'] == sha_file(cl['path']), 'operational_core.sha256_igual_ao_arquivo_instalado': oc['sha256'] == sha_file(oc['path'])}
out['manifesto_ativo'] = man
# ------------------------------------------------------------------ D7.2 kernel + release (argumentos do servidor)
catalog = KernelCatalog(cl['kernel_bundle'], cl.get('kernel_verification'))
st = catalog.status()
out['kernel'] = {'source_sha256_igual_pino': catalog.source_sha == PIN, 'status_keys': sorted(st)[:10], 'files': st.get('files'), 'lean_files': st.get('lean_files'), 'bundle': Path(cl['kernel_bundle']).name}
rel = load_release(MANIFEST, source_sha=catalog.source_sha)
ident = dict(rel.identity)
out['release'] = {'identity': ident, 'e_v407': ident['release'] == 'v407', 'source_igual_pino': ident['source_sha256'] == PIN, 'cluster_sha256_igual_ao_arquivo_instalado': ident['cluster_sha256'] == sha_file(cl['path']), 'operational_core_sha256_igual_ao_arquivo_instalado': ident['operational_core_sha256'] == sha_file(oc['path'])}
ctrl = {}
try:
    load_release(MANIFEST, source_sha='0' * 64)
    ctrl['release_fonte_errada'] = 'NAO_RECUSOU'
except ValueError as e:
    ctrl['release_fonte_errada'] = 'RECUSOU: ' + str(e)[:90]
# ------------------------------------------------------------------ D7.3 pacotes (haiku = shared, haiku55 = haiku_expanded)
STAGING = {'haiku': 'shared', 'haiku55': 'haiku_expanded'}
pk = {}
for name in ('haiku', 'haiku55'):
    d = R / '.iald_runtime' / name
    kw = {'expected_model': HAIKU.model} if name == 'haiku' else {}     # como _load_shared_science_package / _load_haiku_package
    p = load_package(d, canonical_manifest=MANIFEST, source_sha=catalog.source_sha, **kw)
    meas = asdict(p.measurement)
    mj = rd(d / 'manifest.json')
    nc = rd(d / 'native_count.json')
    stg = rd(W / 'app' / 'packages' / STAGING[name] / 'native_count.json')
    pfx = d / 'prefix.md'
    tok = [meas.get('permanent_tokens'), mj['budget']['permanent_tokens'], nc['budget']['permanent_tokens'], stg['budget']['permanent_tokens']]
    pk[name] = {'staging_equivalente': STAGING[name], 'permanent_tokens_lidos': {'carregador': tok[0], 'manifest.json instalado': tok[1], 'native_count.json instalado': tok[2], 'native_count.json do staging (rodada 1)': tok[3]}, 'quatro_fontes_iguais': len(set(tok)) == 1,
                'prefix_bytes_utf8_do_carregador': len(p.prefix.encode('utf-8')), 'prefix_bytes_do_arquivo': pfx.stat().st_size, 'prefix_sha256_do_arquivo': sha_file(pfx), 'manifest.prefix_sha256': mj['prefix_sha256'], 'native_count.prefix_sha256': nc['prefix_sha256'],
                'prefixo_igual_ao_do_staging': sha_file(pfx) == sha_file(W / 'app' / 'packages' / STAGING[name] / 'prefix.md'), 'remaining_tokens': p.available_dynamic_tokens, 'reserved_output_tokens': p.reserved_output_tokens, 'sobra_maior_que_10000': p.available_dynamic_tokens >= 10000,
                'native_count': {k: nc[k] for k in ('status', 'count_requests', 'generation_requests')}, 'deployment_do_manifesto_igual_a_identidade_da_release': mj['deployment'] == ident,
                'prefix_sha256_igual_nas_tres_fontes': sha_file(pfx) == mj['prefix_sha256'] == nc['prefix_sha256'] == p.measurement.prefix_sha256}
    try:
        load_package(d, canonical_manifest=MANIFEST, source_sha='f' * 64, **kw)
        ctrl['pacote_%s_fonte_errada' % name] = 'NAO_RECUSOU'
    except ValueError as e:
        ctrl['pacote_%s_fonte_errada' % name] = 'RECUSOU: ' + str(e)[:90]
out['pacotes'] = pk
# controle negativo (iii): COPIA adulterada do haiku55 (1 byte do prefixo trocado) na minha pasta
tdir = HERE / 'tamper_copy_haiku55'
if tdir.exists():
    shutil.rmtree(tdir)
shutil.copytree(R / '.iald_runtime' / 'haiku55', tdir)
raw = bytearray((tdir / 'prefix.md').read_bytes())
raw[len(raw) // 2] ^= 0x01
(tdir / 'prefix.md').write_bytes(bytes(raw))
try:
    load_package(tdir, canonical_manifest=MANIFEST, source_sha=catalog.source_sha)
    ctrl['pacote_copia_adulterada_1_byte'] = 'NAO_RECUSOU'
except ValueError as e:
    ctrl['pacote_copia_adulterada_1_byte'] = 'RECUSOU: ' + str(e)[:90]
shutil.rmtree(tdir)
ctrl['copia_adulterada_apagada'] = not tdir.exists()
out['controles_negativos'] = ctrl
# ------------------------------------------------------------------ D7.4 contrato JEV
c = load_contract(R)
pe = mf['published_evidence']      # caminhos INSTALADOS do resultado selado e do manifesto de prova, lidos do manifesto ativo
out['jev'] = {'release': c['release'], 'schema': c.get('schema'), 'source_sha256_igual_pino': c['source_sha256'] == PIN, 'result_sha256_igual_ao_um_absoluto_json_instalado': c.get('result_sha256') == sha_file(pe['result']['path']),
              'proof_manifest_sha256_igual_ao_instalado': c.get('proof_manifest_sha256') == sha_file(pe['proof_manifest']['path']),
              'core_packet': {k: c.get('core_packet', {}).get(k) for k in ('um_version', 'arquivo', 'sha256')}, 'core_packet_sha256_igual_ao_arquivo_da_raiz': c.get('core_packet', {}).get('sha256') == sha_file(R / 'core_packet_v407_bound.txt'),
              'sha256_do_arquivo_do_contrato_igual_ao_do_manifesto': sha_file(jev_file) == jc['sha256']}
# ------------------------------------------------------------------ D7.5 extras do verificador (D8): contexto nativo, prompt publico, politica
native, nident = load_native_context(MANIFEST, catalog)
public, meta = CanonicalMemory(Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md'), 'nucleo_kernel', nucleus_manifest=MANIFEST).prompt('', catalog, public=True)
out['extras'] = {'native_bytes': len(native.encode()), 'native_identity_igual_release': nident == ident, 'public_prompt_bytes': len(public.encode()), 'private_atlas_included': meta.get('private_atlas_included'),
                 'politica_AUTOMATIC_ORDER_2_primeiros': list(iald_task_policy.AUTOMATIC_ORDER[:2]), 'native_bytes_igual_ao_native_prefix_do_staging': len(native.encode()) == (W / 'app/native_prefix.md').stat().st_size}
# ------------------------------------------------------------------ D8: INSTALLED_VERIFICATION.json campo a campo
iv_raw = (W / 'INSTALLED_VERIFICATION.json').read_bytes()
iv = json.loads(iv_raw)
so_raw = (W / 'verify_stdout.txt').read_bytes().decode('utf-8').strip().splitlines()
d2 = rd(HERE / 'r2_d1_d6_out.json')['checks']['D2']['ok_no_disco']
rel_json = rd(W / 'app/RELEASE.json')
sub = rd(W / 'receipts/v407-verify-submit.json')['task']['evidence']
cmp = {'chaves_exatas': sorted(iv) == sorted(['status', 'files_verified', 'identity', 'public_commit', 'packages', 'native_bytes', 'public_prompt_bytes', 'JEV_release', 'science_executed', 'provider_calls', 'scope']),
       'status_PASS': iv['status'] == 'PASS', 'files_verified_igual_ao_meu_D2': iv['files_verified'] == d2 == 1782,
       'identity_igual_a_release_medida': iv['identity'] == ident, 'public_commit_igual_cluster_e_RELEASE_json': iv['public_commit'] == cl['commit'] == rel_json['espelho_commit'],
       'haiku55_tokens': iv['packages']['haiku55']['permanent_tokens'] == pk['haiku55']['permanent_tokens_lidos']['carregador'], 'haiku55_bytes': iv['packages']['haiku55']['prefix_bytes'] == pk['haiku55']['prefix_bytes_utf8_do_carregador'] == pk['haiku55']['prefix_bytes_do_arquivo'],
       'haiku_tokens': iv['packages']['haiku']['permanent_tokens'] == pk['haiku']['permanent_tokens_lidos']['carregador'], 'haiku_bytes': iv['packages']['haiku']['prefix_bytes'] == pk['haiku']['prefix_bytes_utf8_do_carregador'] == pk['haiku']['prefix_bytes_do_arquivo'],
       'native_bytes': iv['native_bytes'] == out['extras']['native_bytes'], 'public_prompt_bytes': iv['public_prompt_bytes'] == out['extras']['public_prompt_bytes'], 'JEV_release': iv['JEV_release'] == c['release'] == 'v407',
       'science_executed_false': iv['science_executed'] is False, 'provider_calls_zero': iv['provider_calls'] == 0,
       'verify_stdout_e_a_mesma_linha_json': len(so_raw) == 1 and json.loads(so_raw[0]) == iv,
       'escrito_depois_do_restart_e_do_plano': os.stat(W / 'INSTALLED_VERIFICATION.json').st_mtime > os.stat(W / 'restart.json').st_mtime > os.stat(W / 'maintenance.json').st_mtime,
       'evidencia_submetida_inalterada': all(sha_file(e['path']) == e['sha256'] for e in sub), 'evidencia_submetida': [Path(e['path']).name for e in sub]}
out['D8_comparacao'] = cmp
# provider_calls / science_executed: literal no codigo do verificador ou medicao?
vt = ast.parse((W / 'verify_installed.py').read_text('utf-8'))
lit = {}
for n in ast.walk(vt):
    if isinstance(n, ast.Dict):
        for k, v in zip(n.keys, n.values):
            if isinstance(k, ast.Constant) and k.value in ('provider_calls', 'science_executed'):
                lit[k.value] = {'constante_no_codigo': isinstance(v, ast.Constant), 'valor': v.value if isinstance(v, ast.Constant) else ast.unparse(v)}
out['D8_provider_calls_e_science_executed_no_codigo_do_verificador'] = lit
# ------------------------------------------------------------------ D9 (carregadores)
mods = sorted(STRICT['imports_top'])
PROVIDER_LIBS = {'anthropic', 'openai', 'httpx', 'requests', 'urllib3', 'aiohttp', 'websockets', 'grpc', 'boto3', 'google'}
out['D9'] = {'eventos_socket_contados': STRICT['socket_events'], 'eventos_socket_bloqueados': len(STRICT['socket_blocked']), 'tentativas_de_rede': len(STRICT['socket_blocked']) + len(L.EVENTS['socket_connect_blocked']) + len(L.EVENTS['getaddrinfo_blocked']),
             'aberturas_de_env_bloqueadas': L.EVENTS['env_open_blocked'], 'aberturas_de_segredo_bloqueadas': L.EVENTS['secret_open_blocked'], 'subprocessos_bloqueados': L.EVENTS['subprocess_blocked'], 'escritas_fora_da_pasta_bloqueadas': L.EVENTS['write_outside_blocked'],
             'modulos_de_topo_importados': len(mods), 'bibliotecas_de_provedor_importadas': sorted(set(mods) & PROVIDER_LIBS), 'urllib_importado_sem_uso_de_rede': 'urllib' in mods, 'aberturas_de_leitura': L.EVENTS['opens_read']}
out['segundos'] = round(time.time() - t0, 1)

d7_ok = (out['pino_confere_com_o_um_py_do_cofre'] and all(v for v in man.values() if isinstance(v, bool))
         and man['operational_core.current_release'] == man['active_cluster.release'] == man['jev_control.release'] == 'v407' and man['active_cluster.commit'] == 'bf9017157406afa6b4dc05c6a9d566129e6a6ee4'
         and out['kernel']['source_sha256_igual_pino'] and out['release']['e_v407'] and out['release']['source_igual_pino'] and out['release']['cluster_sha256_igual_ao_arquivo_instalado'] and out['release']['operational_core_sha256_igual_ao_arquivo_instalado']
         and all(v['quatro_fontes_iguais'] and v['prefixo_igual_ao_do_staging'] and v['sobra_maior_que_10000'] and v['deployment_do_manifesto_igual_a_identidade_da_release'] and v['prefix_sha256_igual_nas_tres_fontes'] and v['native_count']['generation_requests'] == 0 for v in pk.values())
         and pk['haiku55']['permanent_tokens_lidos']['carregador'] == 807627 and pk['haiku']['permanent_tokens_lidos']['carregador'] == 415829
         and out['jev']['release'] == 'v407' and out['jev']['source_sha256_igual_pino'] and out['jev']['result_sha256_igual_ao_um_absoluto_json_instalado'] and out['jev']['proof_manifest_sha256_igual_ao_instalado'] and out['jev']['core_packet_sha256_igual_ao_arquivo_da_raiz'] and out['jev']['sha256_do_arquivo_do_contrato_igual_ao_do_manifesto']
         and all(str(v).startswith('RECUSOU') for k, v in ctrl.items() if k != 'copia_adulterada_apagada') and ctrl['copia_adulterada_apagada']
         and out['extras']['native_identity_igual_release'] and out['extras']['private_atlas_included'] is False and out['extras']['politica_AUTOMATIC_ORDER_2_primeiros'] == ['kimi', 'mimo'])
d8_ok = all(v is True for k, v in cmp.items() if k not in ('evidencia_submetida',))
d9_ok = (out['D9']['tentativas_de_rede'] == 0 and out['D9']['aberturas_de_env_bloqueadas'] == 0 and out['D9']['aberturas_de_segredo_bloqueadas'] == 0 and out['D9']['subprocessos_bloqueados'] == 0 and not out['D9']['bibliotecas_de_provedor_importadas'] and not STRICT['socket_events'])
out['PASS_D7'], out['PASS_D8'], out['PASS_D9_carregadores'] = bool(d7_ok), bool(d8_ok), bool(d9_ok)
(HERE / 'r2b_d7_d8_out.json').write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding='utf-8')
print('D7', 'PASS' if d7_ok else 'FAIL', '| D8', 'PASS' if d8_ok else 'FAIL', '| D9(carregadores)', 'PASS' if d9_ok else 'FAIL')
print(json.dumps({k: out[k] for k in ('manifesto_ativo', 'kernel', 'release', 'controles_negativos', 'jev', 'extras', 'D8_comparacao', 'D8_provider_calls_e_science_executed_no_codigo_do_verificador', 'D9', 'segundos')}, ensure_ascii=False, indent=1, default=str)[:7000])
for n, v in pk.items():
    print(n, json.dumps(v, ensure_ascii=False)[:900])
