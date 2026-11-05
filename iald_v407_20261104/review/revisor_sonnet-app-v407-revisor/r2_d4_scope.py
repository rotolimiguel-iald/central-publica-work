"""Revisor sonnet-app-v407-revisor -- RODADA 2: D4(b) varredura de mtime na arvore inteira de C:\\IALD\\projetos_pyhton\\IALD e D4(c) re-medicao PROPRIA do escopo. Somente leitura.
ADAPTADO de check_scope_scan.py do revisor da v406 (-d): janela e contagens da v407; acrescenta (i) as tres visoes de tempo, (ii) os 19 caminhos do B1 nomeados com mtime, (iii) a re-medicao
independente dos agregados (codigo MEU, nao importa transaction.py), (iv) a fonte do estado escrito pelo web novo depois da janela."""
import json, os, sys, time
from datetime import datetime
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import r2lib as L
L.install_guard()
import hashlib
W, R, HERE = L.W, L.R, L.HERE
norm, rd, sha_file = L.norm, L.rd, L.sha_file
fmt = lambda t: datetime.fromtimestamp(t).strftime('%H:%M:%S.%f')[:-3]
t_mnt = os.stat(W / 'maintenance.json').st_mtime
t_rst = os.stat(W / 'restart.json').st_mtime
t_dep0 = os.stat(W / 'deploy_stderr.txt').st_mtime
dep = rd(W / 'deployment.json')
plan = rd(W / 'install_plan.json')
sm = dep['scope_measurement']
installed_at = datetime.fromisoformat(dep['installed_at']).timestamp()
t_now = time.time()
dests = {norm(it['destination']) for it in plan['files']}
baks = {norm(v) for v in dep['backups'].values()}
logs_root = norm(R / 'logs') + os.sep
res = {'tempos': {'deploy_stderr_mtime (inicio do deploy)': fmt(t_dep0), 'maintenance.json mtime (inicio da janela)': fmt(t_mnt), 'installed_at (deployment.json)': fmt(installed_at), 'restart.json mtime (fim da janela)': fmt(t_rst), 'agora': fmt(t_now),
                'janela_estrita_segundos': round(t_rst - t_mnt, 2), 'depois_da_janela_ate_agora_segundos': round(t_now - t_rst, 1)}}

# ------------------------------------------------------------------ varredura da arvore inteira (mtime), sem podar
t0 = time.time()
mods, n_files, n_dirs, truncated = [], 0, 0, False
stack = [str(R)]
while stack:
    cur = stack.pop()
    n_dirs += 1
    try:
        it = os.scandir(cur)
    except OSError:
        continue
    with it:
        for e in it:
            try:
                if e.is_dir(follow_symlinks=False):
                    stack.append(e.path)
                    continue
                n_files += 1
                m = e.stat(follow_symlinks=False).st_mtime
            except OSError:
                continue
            if m >= t_dep0:
                mods.append((e.path, m))
    if time.time() - t0 > 480:
        truncated = True
        break
res['varredura'] = {'arquivos_visitados': n_files, 'diretorios_visitados': n_dirs, 'truncada_por_tempo': truncated, 'segundos': round(time.time() - t0, 1), 'podou_algo': False}

def classify(path):
    n = norm(path)
    if n in dests:
        return 'plano'
    if n in baks:
        return 'backup'
    if n.startswith(logs_root):
        return 'log_do_supervisor_ou_web'
    return 'outro'

buckets = {'pre_janela (deploy_stderr..maintenance.json)': [], 'janela_estrita (maintenance.json..restart.json)': [], 'pos_janela (depois de restart.json)': []}
for p, m in mods:
    if m < t_mnt:
        buckets['pre_janela (deploy_stderr..maintenance.json)'].append((p, m))
    elif m <= t_rst:
        buckets['janela_estrita (maintenance.json..restart.json)'].append((p, m))
    else:
        buckets['pos_janela (depois de restart.json)'].append((p, m))
rel = lambda p: p.replace(str(R) + L.BS, '')
summary = {}
for name, lst in buckets.items():
    cl = {}
    for p, m in lst:
        cl.setdefault(classify(p), []).append((rel(p), fmt(m)))
    summary[name] = {'total': len(lst), 'por_classe': {k: len(v) for k, v in cl.items()}, 'outro': cl.get('outro', []), 'logs': cl.get('log_do_supervisor_ou_web', []), 'backups': len(cl.get('backup', [])), 'plano': len(cl.get('plano', []))}
res['mudancas'] = summary
jan = summary['janela_estrita (maintenance.json..restart.json)']
res['janela_estrita_resultado'] = {'no_plano': jan['plano'], 'backups': jan['backups'], 'logs_do_supervisor': jan['logs'], 'n_logs': len(jan['logs']), 'outros_(achados)': jan['outro']}
# plano: quando foi cada arquivo escrito? (todos dentro da janela estrita?) e quantos do plano NAO mudaram de mtime (bytes ja' iguais)
plan_mtimes = []
for it in plan['files']:
    try:
        plan_mtimes.append(os.stat(it['destination']).st_mtime)
    except OSError:
        pass
res['plano_mtimes'] = {'n': len(plan_mtimes), 'minimo': fmt(min(plan_mtimes)), 'maximo': fmt(max(plan_mtimes)), 'todos_dentro_da_janela_estrita': all(t_mnt <= m <= t_rst for m in plan_mtimes), 'antes_da_janela': sum(1 for m in plan_mtimes if m < t_mnt), 'depois_da_janela': sum(1 for m in plan_mtimes if m > t_rst)}
# backups .bak_<carimbo> do instalador em qualquer lugar de R (orfaos?)
stamp = '20261104_145150'
orph = [rel(p) for p, m in mods if '.bak_' + stamp in os.path.basename(p) and norm(p) not in baks]
res['backups_orfaos_com_o_carimbo_da_instalacao'] = orph

# ------------------------------------------------------------------ B1: os 19 caminhos nomeados
cands = rd(HERE / 'q9_transaction_out.json')['out']['coverage_candidates']
b1 = {}
for label, c in cands.items():
    p = R / c['path']
    files = []
    if p.is_file():
        files = [(str(p), p.stat().st_mtime)]
    elif p.is_dir():
        for dp, dn, fn in os.walk(p):
            for f in fn:
                fp = os.path.join(dp, f)
                try:
                    files.append((fp, os.stat(fp).st_mtime))
                except OSError:
                    pass
    if not files:
        b1[label] = {'path': c['path'], 'existe': p.exists(), 'arquivos': 0}
        continue
    newest = max(m for _, m in files)
    n_pre = sum(1 for _, m in files if m < t_dep0)
    n_prew = sum(1 for _, m in files if t_dep0 <= m < t_mnt)
    n_win = sum(1 for _, m in files if t_mnt <= m <= t_rst)
    n_post = sum(1 for _, m in files if m > t_rst)
    pos = 'DENTRO da janela' if n_win else ('FORA, DEPOIS da janela (web novo)' if n_post else ('FORA, na pre-janela (web antigo/quiet)' if n_prew else 'FORA, ANTES (inalterado)'))
    b1[label] = {'path': c['path'], 'arquivos': len(files), 'arquivos_rodada_1': c['files'], 'mesma_contagem_da_rodada_1': len(files) == c['files'], 'mtime_mais_novo': datetime.fromtimestamp(newest).strftime('%Y-%m-%d %H:%M:%S'), 'antes_do_deploy': n_pre, 'pre_janela': n_prew, 'dentro_da_janela': n_win, 'depois_da_janela': n_post, 'posicao': pos,
                 'plano_escreve_dentro': c['plan_writes_inside']}
res['B1_19_caminhos'] = b1

# ------------------------------------------------------------------ D4(c): re-medicao PROPRIA dos mesmos conjuntos
SKIP = {'Pods', 'build', 'DerivedData', 'xcuserdata', '.gradle', '__pycache__', 'node_modules', '.git'}
def tree(base):
    base = Path(base)
    if base.is_file():
        yield base; return
    if not base.is_dir():
        return
    for top, dirs, files in os.walk(base):
        dirs[:] = sorted(d for d in dirs if d not in SKIP)
        for n in sorted(files):
            if n.lower().endswith('.lock'):
                continue
            yield Path(top) / n
def hash_set(paths):
    out = {}
    for p in sorted(set(paths)):
        k = os.path.normcase(str(p))
        try:
            h, n = hashlib.sha256(), 0
            with open(p, 'rb') as f:
                for ch in iter(lambda: f.read(1 << 20), b''):
                    h.update(ch); n += len(ch)
            out[k] = {'bytes': n, 'sha256': h.hexdigest()}
        except OSError as ex:
            out[k] = {'error': type(ex).__name__}
    return out
def aggregate(files):
    h = hashlib.sha256()
    for k in sorted(files):
        v = files[k]
        h.update((k + '\t' + str(v.get('bytes')) + '\t' + str(v.get('sha256') or v.get('error')) + '\n').encode('utf-8'))
    return h.hexdigest()
rt = R / '.iald_runtime'
state_paths = [p for d in ('app_evaluation', 'app_routing', 'chat_jobs', 'invites', 'monthly_wallet', 'native_push', 'private_media', 'research') for p in tree(rt / d)]
state_paths += [R / 'iald_users.json'] if (R / 'iald_users.json').is_file() else []
for g in ('*.reservas.sqlite3', '*.reservas.sqlite3-wal', '*.reservas.sqlite3-shm', '*.reservas.sqlite3-journal'):
    state_paths += list(R.glob(g))
state_paths += list(tree(R / 'iald_web' / 'data'))
client_paths = []
for t in (('iald-app', 'www'), ('iald-app', 'ios'), ('iald-app', 'android', 'app', 'src'), ('iald_web', 'app')):
    client_paths += list(tree(R.joinpath(*t)))
for f in (('iald-app', 'capacitor.config.json'), ('iald-app', 'package.json'), ('iald-app', 'index.html'), ('iald-app', 'android', 'build.gradle'), ('iald-app', 'android', 'app', 'build.gradle')):
    if R.joinpath(*f).is_file():
        client_paths.append(R.joinpath(*f))
t1 = time.time()
sfiles, cfiles = hash_set(state_paths), hash_set(client_paths)
agg_s, agg_c = aggregate(sfiles), aggregate(cfiles)
unread_s = [k for k, v in sfiles.items() if 'error' in v]
unread_c = [k for k, v in cfiles.items() if 'error' in v]
re = {'tempo_s': round(time.time() - t1, 2),
      'estado': {'arquivos': len(sfiles), 'bytes': sum(v.get('bytes', 0) for v in sfiles.values()), 'agregado_agora': agg_s, 'agregado_after_do_deployment': sm['state_aggregate_after'], 'agregado_before_do_deployment': sm['state_aggregate_before'], 'igual_ao_after': agg_s == sm['state_aggregate_after'], 'arquivos_no_deployment': sm['state_files'], 'bytes_no_deployment': sm['state_bytes'], 'ilegiveis': unread_s},
      'cliente': {'arquivos': len(cfiles), 'bytes': sum(v.get('bytes', 0) for v in cfiles.values()), 'agregado_agora': agg_c, 'agregado_after_do_deployment': sm['client_aggregate_after'], 'agregado_before_do_deployment': sm['client_aggregate_before'], 'igual_ao_after': agg_c == sm['client_aggregate_after'], 'arquivos_no_deployment': sm['client_files'], 'bytes_no_deployment': sm['client_bytes'], 'ilegiveis': unread_c}}
# tabela do estado: cada arquivo com mtime e posicao frente a janela (para explicar qualquer diferenca)
rows = []
for p in sorted(set(state_paths), key=lambda x: os.path.normcase(str(x))):
    try:
        m = os.stat(p).st_mtime
    except OSError:
        continue
    pos = 'depois' if m > t_rst else ('dentro' if m >= t_mnt else ('pre_janela' if m >= t_dep0 else 'antes'))
    rows.append({'path': rel(str(p)), 'bytes': sfiles[os.path.normcase(str(p))].get('bytes'), 'mtime': datetime.fromtimestamp(m).strftime('%Y-%m-%d %H:%M:%S'), 'posicao': pos})
re['estado_por_posicao'] = {k: sum(1 for r in rows if r['posicao'] == k) for k in ('antes', 'pre_janela', 'dentro', 'depois')}
re['estado_modificados_depois_da_janela'] = [r for r in rows if r['posicao'] == 'depois']
re['estado_modificados_na_pre_janela_ou_dentro'] = [r for r in rows if r['posicao'] in ('pre_janela', 'dentro')]
crow = []
for p in sorted(set(client_paths), key=lambda x: os.path.normcase(str(x))):
    try:
        m = os.stat(p).st_mtime
    except OSError:
        continue
    if m >= t_dep0:
        crow.append({'path': rel(str(p)), 'mtime': datetime.fromtimestamp(m).strftime('%Y-%m-%d %H:%M:%S')})
re['cliente_modificados_desde_o_inicio_do_deploy'] = crow
res['re_medicao'] = re
# corroboracao com a minha medicao da rodada 1 (antes da instalacao): bytes totais
q9 = rd(HERE / 'q9_transaction_out.json')['out']['live']
res['corroboracao_rodada_1'] = {'estado_bytes_rodada_1': q9['state_bytes'], 'cliente_bytes_rodada_1': q9['client_bytes'], 'estado_arquivos_rodada_1': q9['state_files'], 'cliente_arquivos_rodada_1': q9['client_files']}
res['guard_events'] = {k: (v if not isinstance(v, list) else len(v)) for k, v in L.EVENTS.items()}
(HERE / 'r2_d4_scope_out.json').write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
print(json.dumps({k: res[k] for k in ('tempos', 'varredura', 'janela_estrita_resultado', 'plano_mtimes', 'backups_orfaos_com_o_carimbo_da_instalacao')}, ensure_ascii=False, indent=1)[:5000])
print('--- classes por bucket:', json.dumps({k: {kk: vv for kk, vv in v.items() if kk in ('total', 'por_classe')} for k, v in summary.items()}, ensure_ascii=False))
print('--- re-medicao:', json.dumps({k: {kk: vv for kk, vv in v.items()} for k, v in (('estado', re['estado']), ('cliente', re['cliente']))}, ensure_ascii=False)[:2600])
print('--- estado por posicao:', re['estado_por_posicao'])
