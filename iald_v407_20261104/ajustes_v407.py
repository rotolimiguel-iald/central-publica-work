# -*- coding: utf-8 -*-
"""Ajustes da v407 sobre as ferramentas copiadas da v406 (registro do que mudou; cada troca exige exatamente uma ocorrencia).
ORDEM_006 + LICOES_v406 / LICOES_v406_AO_LADO: (1) janela P2 desliza de novo (sai _v402, com limites/diz/nao_diz mantidos na capsula compacta);
(2) F1 do parecer da v406: protected_fields protege registros de estatuto PLANOS de ate 500 B (ex.: projecao_transversal_v404/name_status);
(3) o escopo da instalacao passa a ser MEDIDO (accounts_modified, bench_restarted, client_files_changed deixam de ser constantes False);
(4) textos de versao, semente da busca, ordem do operador byte a byte.
Hash e commit lidos por script: o pino do um.py vem do selo do cofre; o commit curto da ORDEM_006 e' resolvido no git do espelho e conferido com origin/main."""
import hashlib
import json
import subprocess
from pathlib import Path

W = Path(__file__).resolve().parent
REPO = Path(r"C:\IALD\Artigo\the_boundary")
VAULT = Path(r"C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v407")
COMMIT_CURTO = "bf901715"            # ORDEM_006: o espelho the_boundary no commit bf901715
OPERADOR = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_03nov_prossigamos_com_tudo_ratifico_tudo_orquestrador_claude_app_readme_pinado_teste_d_verbatim.txt")
OPERADOR_SHA16 = "b89e4c909f37e163"  # ORDEM_006
feito = []


def git(*args):
    p = subprocess.run(["git", "-C", str(REPO), *args], capture_output=True)
    assert p.returncode == 0, (args, p.stderr.decode("utf-8", "replace"))
    return p.stdout.decode("utf-8").strip()


def troca(arq, pares):
    p = W / arq
    raw = p.read_bytes()
    t = raw.decode("utf-8")
    eol = "\r\n" if "\r\n" in t else "\n"
    for velho, novo in pares:
        velho, novo = velho.replace("\n", eol), novo.replace("\n", eol)
        assert t.count(velho) == 1, (arq, t.count(velho), velho[:90])
        t = t.replace(velho, novo)
    p.write_bytes(t.encode("utf-8"))
    feito.append(arq)


# ---------------------------------------------------------------- RELEASE.json (release, commit, pino lidos por script)
commit = git("rev-parse", "--verify", COMMIT_CURTO + "^{commit}")
assert len(commit) == 40 and commit == git("rev-parse", "origin/main"), "o commit da ORDEM_006 nao e' o origin/main do espelho"
seal = json.loads((VAULT / "um_absoluto_selo.json").read_bytes())
assert seal["um_version"] == "v407" and seal["fail_closed_selftest"] == "FAIL_CLOSED_SELFTEST_PASSED"
pino = seal["sha256"]["um.py"]
assert hashlib.sha256((VAULT / "um.py").read_bytes()).hexdigest() == pino
assert pino.startswith("833121339e649f71"), "o pino lido do selo difere do pino da ORDEM_006"
(W / "app" / "RELEASE.json").write_text(json.dumps({"release": "v407", "espelho_commit": commit, "um_py_sha256": pino}, indent=2), encoding="utf-8")
feito.append("app/RELEASE.json")

# ---------------------------------------------------------------- release_cfg.py: a janela P2 desliza (sai _v402)
troca("release_cfg.py", [
    ("SHARED_P2_SUFFIXES = ('_v402', '_v403', '_v404', '_v405', '_v406')\nP2_RETIRED_LITERAL_SUFFIXES = ('_v401',)",
     "# 04/11/2026 (v407, ORDEM_006 e LICOES_v406): a janela DESLIZA de novo. Sai _v402 (a folga minima declarada da v406 foi 41975 B e uma release de ~30 KB consome tres quartos dela); entram os novos _v407.\n"
     "# _v403 so' sai se o shared nao couber na menor folga medida com a reserva declarada (decidir ANTES do finalize). Os topicos que saem mantem limites/diz/nao_diz literais na capsula compacta.\n"
     "SHARED_P2_SUFFIXES = ('_v403', '_v404', '_v405', '_v406', '_v407')\n"
     "P2_RETIRED_LITERAL_SUFFIXES = ('_v401', '_v402')"),
])

# ---------------------------------------------------------------- haiku_codec.py: F1 (registro de estatuto plano nao vira so' ponteiro)
troca("app/build/haiku_codec.py", [
    ("def protected_fields(value, pointer=''):\n",
     "STATUS_KEY = re.compile(r'status|estatuto|verdict|veredito', re.I)\n"
     "STATUS_RECORD_MAX = 500\n"
     "\n"
     "\n"
     "def status_record(key, item):\n"
     "    \"\"\"v407 (F1 do parecer da v406): um registro de estatuto e' um dict PLANO de escalares (ex.: name_status = {estado: PROVISORIO, aceito_pelo_operador: ...}).\n"
     "    Sem esta regra as chaves-filhas (estado, aceito_...) nao casam com ESSENTIAL e o registro inteiro virava so' ponteiro na base compacta do haiku55.\n"
     "    Limite de 500 B: protege os registros pequenos (medido na fonte da v407: 59 de 217 dicts planos de estatuto, 17853 B); os catalogos 'statuses' (ate 6 KB) seguem recuperaveis pelo ponteiro.\"\"\"\n"
     "    return (isinstance(item, dict) and bool(item) and STATUS_KEY.search(str(key)) is not None\n"
     "            and all(not isinstance(v, (dict, list)) for v in item.values()) and len(dump(item)) <= STATUS_RECORD_MAX)\n"
     "\n"
     "\n"
     "def protected_fields(value, pointer=''):\n"),
    ("            if WHOLE_FIELD.search(key) or (ESSENTIAL.search(key) and not isinstance(item, (dict, list))):\n                result[location] = item\n",
     "            if WHOLE_FIELD.search(key) or (ESSENTIAL.search(key) and not isinstance(item, (dict, list))) or status_record(key, item):\n                result[location] = item\n"),
])

# ---------------------------------------------------------------- transaction.py: o escopo da instalacao e' MEDIDO (antes/depois da escrita, na janela com o web parado)
SCOPE_BLOCK = r'''# --- v407: escopo da instalacao MEDIDO. Na v406, accounts_modified, bench_restarted e client_files_changed eram constantes False deste arquivo (licao 5 da v406).
# Aqui sao medicoes SOMENTE LEITURA, antes e depois da escrita, dentro da janela com o web parado. Falha de leitura vira None (nao medido), nunca False.
SCOPE_STATE_DIRS = ('app_evaluation', 'app_routing', 'chat_jobs', 'invites', 'monthly_wallet', 'native_push', 'private_media', 'research')   # sob .iald_runtime
SCOPE_STATE_FILES = ('iald_users.json',)
SCOPE_STATE_GLOBS = ('*.reservas.sqlite3', '*.reservas.sqlite3-wal', '*.reservas.sqlite3-shm', '*.reservas.sqlite3-journal')
SCOPE_STATE_TREES = (('iald_web', 'data'),)
SCOPE_CLIENT_TREES = (('iald-app', 'www'), ('iald-app', 'ios'), ('iald-app', 'android', 'app', 'src'), ('iald_web', 'app'))
SCOPE_CLIENT_FILES = (('iald-app', 'capacitor.config.json'), ('iald-app', 'package.json'), ('iald-app', 'index.html'),
                      ('iald-app', 'android', 'build.gradle'), ('iald-app', 'android', 'app', 'build.gradle'))
SCOPE_SKIP_DIRS = frozenset(('Pods', 'build', 'DerivedData', 'xcuserdata', '.gradle', '__pycache__', 'node_modules', '.git'))
SCOPE_BENCH_PORTS = (18765, 18766)
SCOPE_LOCAL_MODEL_PORT = 8081


def _scope_walk(base):
    if base.is_file():
        yield base
        return
    if not base.is_dir():
        return
    for top, dirs, files in os.walk(base):
        dirs[:] = sorted(d for d in dirs if d not in SCOPE_SKIP_DIRS)
        for name in sorted(files):
            yield Path(top) / name


def _scope_files(paths):
    out = {}
    for path in paths:
        key = os.path.normcase(str(path))
        try:
            h, n = hashlib.sha256(), 0
            with open(path, 'rb') as f:
                for chunk in iter(lambda: f.read(1 << 20), b''):
                    h.update(chunk)
                    n += len(chunk)
            out[key] = {'bytes': n, 'sha256': h.hexdigest()}
        except OSError as exc:
            out[key] = {'error': type(exc).__name__ + ': ' + str(exc)[:160]}
    return out


def _scope_listeners(port):
    import psutil
    pids = sorted({c.pid for c in psutil.net_connections(kind='tcp') if c.status == psutil.CONN_LISTEN and c.laddr.port == port and c.pid})
    rows = []
    for pid in pids:
        try:
            rows.append({'pid': pid, 'create_time': psutil.Process(pid).create_time()})
        except psutil.Error:
            rows.append({'pid': pid, 'create_time': None})
    return rows


def scope_snapshot(destinations):
    """So leitura; nunca levanta. Cada grupo que falhar entra em 'errors' e o campo correspondente sai None."""
    started = time.monotonic()
    snap = {'errors': []}
    runtime = ROOT / '.iald_runtime'
    try:
        paths = [p for name in SCOPE_STATE_DIRS for p in _scope_walk(runtime / name)]
        paths += [ROOT / f for f in SCOPE_STATE_FILES if (ROOT / f).is_file()]
        paths += [p for g in SCOPE_STATE_GLOBS for p in ROOT.glob(g)]
        paths += [p for t in SCOPE_STATE_TREES for p in _scope_walk(ROOT.joinpath(*t))]
        snap['state'] = _scope_files(sorted(set(paths)))
    except Exception as exc:
        snap['state'] = {}
        snap['errors'].append({'group': 'state', 'error': type(exc).__name__ + ': ' + str(exc)[:160]})
    try:
        paths = [p for t in SCOPE_CLIENT_TREES for p in _scope_walk(ROOT.joinpath(*t))]
        paths += [ROOT.joinpath(*f) for f in SCOPE_CLIENT_FILES if ROOT.joinpath(*f).is_file()]
        snap['client'] = _scope_files(sorted(set(paths)))
    except Exception as exc:
        snap['client'] = {}
        snap['errors'].append({'group': 'client', 'error': type(exc).__name__ + ': ' + str(exc)[:160]})
    snap['listeners'] = {}
    try:
        for port in SCOPE_BENCH_PORTS + (SCOPE_LOCAL_MODEL_PORT,):
            snap['listeners'][str(port)] = _scope_listeners(port)
    except Exception as exc:
        snap['listeners'] = {}
        snap['errors'].append({'group': 'listeners', 'error': type(exc).__name__ + ': ' + str(exc)[:160]})
    dest = {os.path.normcase(str(Path(d))) for d in destinations}
    snap['plan_overlap'] = sorted((set(snap['state']) | set(snap['client'])) & dest)
    snap['seconds'] = round(time.monotonic() - started, 3)
    return snap


def _scope_aggregate(files):
    h = hashlib.sha256()
    for key in sorted(files):
        v = files[key]
        h.update((key + '\t' + str(v.get('bytes')) + '\t' + str(v.get('sha256') or v.get('error')) + '\n').encode('utf-8'))
    return h.hexdigest()


def scope_compare(before, after):
    errors = list(before.get('errors', [])) + list(after.get('errors', []))
    failed = {e['group'] for e in errors}

    def group(name):
        a, b = before.get(name, {}), after.get(name, {})
        changed = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
        unreadable = sorted({k for side in (a, b) for k, v in side.items() if 'error' in v})
        ok = name not in failed and bool(a) and bool(b) and not unreadable
        return changed, unreadable, ok, a, b

    s_changed, s_unreadable, s_ok, s_a, s_b = group('state')
    c_changed, c_unreadable, c_ok, c_a, c_b = group('client')
    la, lb = before.get('listeners', {}), after.get('listeners', {})
    l_ok = 'listeners' not in failed and bool(la) and bool(lb)
    bench_changed = [str(p) for p in SCOPE_BENCH_PORTS if la.get(str(p)) != lb.get(str(p))]
    model_changed = la.get(str(SCOPE_LOCAL_MODEL_PORT)) != lb.get(str(SCOPE_LOCAL_MODEL_PORT))
    return {
        'accounts_modified': True if s_changed else (False if s_ok else None),
        'bench_restarted': (True if bench_changed else False) if l_ok else None,
        'client_files_changed': True if c_changed else (False if c_ok else None),
        'scope_measurement': {
            'method': 'sha256 de cada arquivo (estado e cliente) e pid+create_time de quem escuta as portas, antes e depois da escrita, dentro da janela com o web parado; somente leitura',
            'state_files': len(s_a), 'state_bytes': sum(v.get('bytes', 0) for v in s_a.values()),
            'state_aggregate_before': _scope_aggregate(s_a), 'state_aggregate_after': _scope_aggregate(s_b),
            'state_changed': s_changed, 'state_unreadable': s_unreadable,
            'client_files': len(c_a), 'client_bytes': sum(v.get('bytes', 0) for v in c_a.values()),
            'client_aggregate_before': _scope_aggregate(c_a), 'client_aggregate_after': _scope_aggregate(c_b),
            'client_changed': c_changed, 'client_unreadable': c_unreadable,
            'bench_ports': [str(p) for p in SCOPE_BENCH_PORTS], 'bench_changed': bench_changed,
            'bench_running_before': {p: bool(la.get(p)) for p in map(str, SCOPE_BENCH_PORTS)}, 'bench_running_after': {p: bool(lb.get(p)) for p in map(str, SCOPE_BENCH_PORTS)},
            'local_model_port': SCOPE_LOCAL_MODEL_PORT, 'local_model_changed': model_changed,
            'listeners_before': la, 'listeners_after': lb,
            'plan_overlap_before': before.get('plan_overlap', []), 'plan_overlap_after': after.get('plan_overlap', []),
            'errors': errors, 'seconds_before': before.get('seconds'), 'seconds_after': after.get('seconds'),
        }}


def apply_plan(plan_path):
'''
troca("transaction.py", [
    ("import os\nimport sqlite3\n", "import os\nimport sqlite3\nimport time\n"),
    ("def apply_plan(plan_path):\n", SCOPE_BLOCK),
    ("    quiet()\n    old, new, backups, written = {}, {}, {}, []\n",
     "    quiet()\n    plan_dests = [i['destination'] for i in plan['files']]\n    scope_before = scope_snapshot(plan_dests)   # v407: medido dentro da janela, antes de escrever\n    old, new, backups, written = {}, {}, {}, []\n"),
    ("'files':{str(p):digest(v) for p,v in new.items()}, 'accounts_modified':False,\n              'bench_restarted':False, 'client_files_changed':False}\n",
     "'files':{str(p):digest(v) for p,v in new.items()},\n              'accounts_modified':scope['accounts_modified'], 'bench_restarted':scope['bench_restarted'],\n              'client_files_changed':scope['client_files_changed'], 'scope_measurement':scope['scope_measurement']}\n"),
    ("    report = {'status':'INSTALLED_RESTART_REQUIRED'",
     "    scope = scope_compare(scope_before, scope_snapshot(plan_dests))   # v407: medido de novo, ainda dentro da janela, depois de escrever\n    report = {'status':'INSTALLED_RESTART_REQUIRED'"),
])

# ---------------------------------------------------------------- textos de versao, semente da busca
troca("task.py", [
    ('Mapa de rotas: consulta "app release v406 ciencia haiku55 janela P2 shared" (0 rotas) em 03/11 (1748 registros). Pipeline de referência: work/iald_v405_20261102 (instalada v405, aceita por revisores distintos do construtor). Mudanças desta release: R3-1 e R3-2 da LICOES_v405, janela P2 do shared deslizada (ORDEM_004 da gerência c1) com limites/diz/nao_diz mantidos na cápsula compacta.',
     'Mapa de rotas: consultas "app.release" (8 rotas; nenhuma app.release.v407) e "v407" (27 rotas; nenhuma do app) em 04/11 (ultima seq 1785). Pipeline de referência: work/iald_v406_20261103 (instalada v406, aceita por revisores distintos do construtor). Mudanças desta release: janela P2 do shared deslizada de novo (ORDEM_006 da cadeia de selo; sai _v402) com limites/diz/nao_diz mantidos na cápsula compacta; F1 do parecer da v406 (protected_fields passa a proteger registros de estatuto planos de até 500 B, como name_status); escopo da instalação MEDIDO (accounts_modified, bench_restarted e client_files_changed deixam de ser constantes).'),
])
troca("run_construcao.sh", [("Construcao da release do app (v406)", "Construcao da release do app (v407)")])
troca("run_etapa1_v407.sh", [("# v406, etapa 1 (offline)", "# v407, etapa 1 (offline)")])
troca("run_etapa2_v407.sh", [("# v406, etapa 2:", "# v407, etapa 2:"), ("cp busca_stdout.txt BUSCA_EXERCITADA_v406.txt", "cp busca_stdout.txt BUSCA_EXERCITADA_v407.txt")])
troca("exercita_busca.py", [("random.Random(20261103)", "random.Random(20261104)"), ('"semente 20261103"', '"semente 20261104"')])

# ---------------------------------------------------------------- a ordem do operador, byte a byte (task.py exige bytes identicos)
raw = OPERADOR.read_bytes()
assert hashlib.sha256(raw).hexdigest()[:16] == OPERADOR_SHA16, "o verbatim do operador difere do pino da ORDEM_006"
for n in ("ORDEM_DO_OPERADOR.txt", "ORIGINAL.txt"):
    with (W / n).open("xb") as f:
        f.write(raw)
    assert (W / n).read_bytes() == raw
feito += ["ORDEM_DO_OPERADOR.txt", "ORIGINAL.txt"]
print(json.dumps({"ajustados": feito, "pino_um_py": pino[:16], "commit": commit, "ordem_do_operador_sha16": hashlib.sha256(raw).hexdigest()[:16]}, ensure_ascii=False))
