"""Revisor sonnet-app-v407-revisor -- Q9: transaction.py (escopo MEDIDO). Somente leitura no runtime vivo; os testes de mutacao usam uma RAIZ DE BRINQUEDO dentro desta pasta.
Escrito por mim (nao herda o teste do construtor). Importa W\\transaction.py (so' define funcoes; sem efeito no import) e troca T.ROOT por uma pasta temporaria minha.
Nao inicia nem mata processo; nao chama apply_plan; nao toca em deployment.json."""
import ast, ctypes, difflib, hashlib, json, os, random, re, shutil, sys, time
from ctypes import wintypes
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
W = Path(r'C:\IALD\Central de Patentes\work\iald_v407_20261104')
W6 = Path(r'C:\IALD\Central de Patentes\work\iald_v406_20261103')
R = Path(r'C:\IALD\projetos_pyhton\IALD')
TOY = HERE / 'toy_root_q9'
sha = lambda b: hashlib.sha256(b).hexdigest()
chk, out = [], {}


def _guard(event, args):
    # nada de rede, subprocesso, os.system; nada escrito fora desta pasta
    if event in ('socket.connect', 'socket.getaddrinfo', 'subprocess.Popen', 'os.system'):
        raise RuntimeError('blocked ' + event)
    if event == 'open':
        path, mode, flags = args
        if isinstance(path, int):
            return
        p = Path(os.fsdecode(path)).resolve()
        if p.name in ('.env', 'iald_stack_v7.py', 'iald_psion_state.json') or p.name.startswith('.env'):
            raise RuntimeError('private input forbidden')
        writing = (isinstance(mode, str) and any(c in mode for c in 'wax+')) or (isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC))
        if writing and not p.is_relative_to(HERE):
            raise RuntimeError('write outside reviewer folder: ' + str(p))


sys.addaudithook(_guard)


def ck(name, ok, **info):
    chk.append({'name': name, 'pass': bool(ok), **info})


# ======================================================== A. diff contra a v406 (so' o permitido?) -- (vii)
t7 = (W / 'transaction.py').read_bytes().decode('utf-8')
t6 = (W6 / 'transaction.py').read_bytes().decode('utf-8')
out['sizes'] = {'v406_bytes': len(t6.encode()), 'v407_bytes': len(t7.encode()), 'v406_sha16': sha(t6.encode())[:16], 'v407_sha16': sha(t7.encode())[:16], 'eol_v406': 'CRLF' if '\r\n' in t6 else 'LF', 'eol_v407': 'CRLF' if '\r\n' in t7 else 'LF'}
l6, l7 = t6.splitlines(keepends=True), t7.splitlines(keepends=True)
sm = difflib.SequenceMatcher(None, l6, l7, autojunk=False)
hunks = []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != 'equal':
        hunks.append({'op': tag, 'v406_lines': [i1 + 1, i2], 'v407_lines': [j1 + 1, j2], 'removed': ''.join(l6[i1:i2])[:300], 'added_first_line': (''.join(l7[j1:j2]).splitlines() or [''])[0][:160], 'added_n_lines': j2 - j1})
out['diff_hunks'] = hunks
EXPECT_ADDED = {'import time': 1, '# --- v407: escopo': 1}
# classificar cada hunk
cls = []
for h in hunks:
    first = h['added_first_line']
    if h['op'] == 'insert' and first.strip() == 'import time':
        cls.append('import_time')
    elif h['op'] == 'insert' and first.startswith('# --- v407: escopo da instalacao MEDIDO'):
        cls.append('scope_block')
    elif h['op'] == 'insert' and 'plan_dests = [i[' in ''.join(l7[h['v407_lines'][0] - 1:h['v407_lines'][1]]):
        cls.append('apply_plan_scope_before')
    elif h['op'] == 'replace' and "'accounts_modified':False" in h['removed'].replace(' ', '') or (h['op'] == 'replace' and 'accounts_modified' in h['removed']):
        cls.append('apply_plan_report_fields')
    elif h['op'] == 'insert' and 'scope = scope_compare(' in ''.join(l7[h['v407_lines'][0] - 1:h['v407_lines'][1]]):
        cls.append('apply_plan_scope_after')
    else:
        cls.append('UNEXPECTED')
out['diff_hunk_classes'] = cls
ck('Q9.vii_diff_has_only_the_five_expected_hunks', sorted(cls) == sorted(['import_time', 'scope_block', 'apply_plan_scope_before', 'apply_plan_scope_after', 'apply_plan_report_fields']), classes=cls, n=len(hunks))
# reconstruir a v406 a partir da v407 revertendo exatamente as 5 mudancas => bytes iguais
rev = t7
rev = rev.replace('import sqlite3\nimport time\n', 'import sqlite3\n', 1)
a = rev.index('# --- v407: escopo da instalacao MEDIDO.')
b = rev.index('def apply_plan(plan_path):')
rev = rev[:a] + rev[b:]
rev = rev.replace("    plan_dests = [i['destination'] for i in plan['files']]\n    scope_before = scope_snapshot(plan_dests)   # v407: medido dentro da janela, antes de escrever\n", '', 1)
rev = rev.replace("    scope = scope_compare(scope_before, scope_snapshot(plan_dests))   # v407: medido de novo, ainda dentro da janela, depois de escrever\n", '', 1)
rev = rev.replace("'files':{str(p):digest(v) for p,v in new.items()},\n              'accounts_modified':scope['accounts_modified'], 'bench_restarted':scope['bench_restarted'],\n              'client_files_changed':scope['client_files_changed'], 'scope_measurement':scope['scope_measurement']}\n",
                  "'files':{str(p):digest(v) for p,v in new.items()}, 'accounts_modified':False,\n              'bench_restarted':False, 'client_files_changed':False}\n", 1)
out['reverse_engineered_equals_v406_bytes'] = rev.encode() == t6.encode()
ck('Q9.vii_reverting_the_5_known_changes_gives_v406_byte_for_byte', rev.encode() == t6.encode(), v406_sha16=sha(t6.encode())[:16], reverted_sha16=sha(rev.encode())[:16])
# o resto de apply_plan (de 'def apply_plan' ate 'quiet()') e do 'old, new, backups' ate 'raise' identico
def fn_body(t, name):
    m = re.search(r'(?ms)^def %s\(.*?(?=^def |\Z)' % re.escape(name), t)
    return m.group(0)
b6, b7 = fn_body(t6, 'apply_plan'), fn_body(t7, 'apply_plan')
core_part = lambda s: s[s.index('old, new, backups, written'):s.index('    scope = ') if '    scope = ' in s else s.index('    report = {')]
ck('Q9.vii_apply_plan_quiet_validation_backups_rollback_block_identical', core_part(b6) == core_part(b7) and b6[:b6.index('    quiet()')] == b7[:b7.index('    quiet()')], n_chars=len(core_part(b7)))
# funcoes que nao sao de escopo: identicas
ast6, ast7 = ast.parse(t6), ast.parse(t7)
f6 = {n.name: ast.dump(n) for n in ast6.body if isinstance(n, ast.FunctionDef)}
f7 = {n.name: ast.dump(n) for n in ast7.body if isinstance(n, ast.FunctionDef)}
changed_funcs = sorted(k for k in f6 if f6[k] != f7.get(k))
new_funcs = sorted(set(f7) - set(f6))
out['functions'] = {'changed_vs_v406': changed_funcs, 'new': new_funcs, 'removed': sorted(set(f6) - set(f7))}
ck('Q9.vii_only_apply_plan_changed_and_new_functions_are_scope', changed_funcs == ['apply_plan'] and sorted(new_funcs) == ['_scope_aggregate', '_scope_files', '_scope_listeners', '_scope_walk', 'scope_compare', 'scope_snapshot'] and not (set(f6) - set(f7)), **out['functions'])
for fn in ('atomic', 'backup', 'write_evidence', 'quiet', 'local_json', 'bench_snapshot', 'digest'):
    if f6[fn] != f7[fn]:
        ck('Q9.vii_unchanged_' + fn, False)
# maintenance.py / deploy_controlled.py / verify_installed.py / review_app.py: bytes
same = {}
for nm in ('maintenance.py', 'deploy_controlled.py', 'verify_installed.py'):
    same[nm] = {'equal_v406': (W / nm).read_bytes() == (W6 / nm).read_bytes(), 'sha16': sha((W / nm).read_bytes())[:16]}
same['review/review_app.py'] = {'equal_v406': (W / 'review/review_app.py').read_bytes() == (W6 / 'review/review_app.py').read_bytes(), 'sha16': sha((W / 'review/review_app.py').read_bytes())[:16]}
out['Q10_tools_equal_v406'] = same

# ======================================================== B. (i) so' leem: AST das funcoes de escopo
scope_fns = [n for n in ast7.body if isinstance(n, ast.FunctionDef) and (n.name.startswith('_scope') or n.name.startswith('scope_'))]
calls = {}
for fn in scope_fns:
    for node in ast.walk(fn):
        if isinstance(node, ast.Call):
            f = node.func
            nm = f.id if isinstance(f, ast.Name) else (ast.unparse(f) if isinstance(f, ast.Attribute) else type(f).__name__)
            calls.setdefault(nm, set()).add(fn.name)
out['scope_functions'] = [f.name for f in scope_fns]
out['scope_calls'] = {k: sorted(v) for k, v in sorted(calls.items())}
FORBID = re.compile(r'(?:^|\.)(write|write_text|write_bytes|remove|unlink|rmdir|rmtree|rename|replace|makedirs|mkdir|touch|chmod|utime|symlink|copy|copyfile|copytree|move|kill|terminate|suspend|resume|wait|Popen|run|call|system|check_output|connect|send|sendall|bind|listen|request|urlopen|execute|executemany|executescript|fsync|truncate|flush|dump|writelines)$')
bad_calls = sorted(k for k in calls if FORBID.search(k))
ck('Q9.i_scope_functions_make_no_mutating_call_static', not bad_calls, bad=bad_calls, calls=sorted(calls))
# open() so' em 'rb'
opens = []
for fn in scope_fns:
    for node in ast.walk(fn):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'open':
            mode = node.args[1].value if len(node.args) > 1 and isinstance(node.args[1], ast.Constant) else None
            opens.append((fn.name, mode))
ck('Q9.i_every_open_in_scope_functions_is_rb', opens and all(m == 'rb' for _, m in opens), opens=opens)

# ======================================================== C. carregar o modulo com ROOT de brinquedo
import importlib.util
spec = importlib.util.spec_from_file_location('transaction_rev', W / 'transaction.py')
T = importlib.util.module_from_spec(spec)
spec.loader.exec_module(T)
ck('Q9.import_has_no_side_effect_and_defaults', T.ROOT == R and T.SCOPE_BENCH_PORTS == (18765, 18766) and T.SCOPE_LOCAL_MODEL_PORT == 8081 and not (W / 'deployment.json').exists())


def make_toy():
    if TOY.exists():
        shutil.rmtree(TOY)
    for d in T.SCOPE_STATE_DIRS:
        (TOY / '.iald_runtime' / d).mkdir(parents=True)
        (TOY / '.iald_runtime' / d / (d + '.dat')).write_bytes(b'state-' + d.encode())
    (TOY / '.iald_runtime/monthly_wallet/web-runtime.lock').write_bytes(b'lock0')
    (TOY / '.iald_runtime/monthly_wallet/sub').mkdir()
    (TOY / '.iald_runtime/monthly_wallet/sub/ledger.db').write_bytes(b'ledger')
    (TOY / 'iald_users.json').write_bytes(b'{"users":[]}')
    (TOY / 'iald_uso_claude.json.reservas.sqlite3').write_bytes(b'sq')
    (TOY / 'iald_uso_claude.json.reservas.sqlite3-wal').write_bytes(b'wal')
    (TOY / 'iald_web/data').mkdir(parents=True)
    (TOY / 'iald_web/data/users.json').write_bytes(b'{}')
    for p in (('iald-app', 'www'), ('iald-app', 'ios', 'App'), ('iald-app', 'android', 'app', 'src', 'main'), ('iald_web', 'app')):
        (TOY.joinpath(*p)).mkdir(parents=True)
    (TOY / 'iald-app/www/app.js').write_bytes(b'console.log(1)')
    (TOY / 'iald-app/ios/App/Info.plist').write_bytes(b'<plist/>')
    (TOY / 'iald-app/ios/Pods').mkdir()
    (TOY / 'iald-app/ios/Pods/skipme.txt').write_bytes(b'pods')
    (TOY / 'iald-app/android/app/src/main/A.java').write_bytes(b'class A{}')
    (TOY / 'iald_web/app/a.py').write_bytes(b'x=1')
    (TOY / 'iald-app/capacitor.config.json').write_bytes(b'{}')
    (TOY / 'iald-app/package.json').write_bytes(b'{}')
    return [str(TOY / 'canonical_releases/v999/x.bin')]


def fresh_listeners(before, after):
    """substitui SO' a leitura de listeners (nao inicio processo): a funcao real e' exercida no teste vivo mais abaixo"""
    seq = iter([before, after])
    state = {}
    def fake(port):
        key = port
        return state.setdefault(('cur',), None) or []
    return fake


T.ROOT = TOY
dests = make_toy()
real_listeners = T._scope_listeners
LST = {'cur': {'18765': [], '18766': [], '8081': [{'pid': 11, 'create_time': 1.5}]}}
T._scope_listeners = lambda port: LST['cur'][str(port)]


def snap():
    return T.scope_snapshot(dests)


def tri(r):
    return (r['accounts_modified'], r['bench_restarted'], r['client_files_changed'])


# --- B1 sem mudanca
s1, s2 = snap(), snap()
r = T.scope_compare(s1, s2)
ck('Q9.v_toy_no_change_all_false', tri(r) == (False, False, False), tri=tri(r), state_files=r['scope_measurement']['state_files'], client_files=r['scope_measurement']['client_files'],
   skipped_pods_and_lock=all(('skipme.txt' not in k and 'web-runtime.lock' not in k) for k in s1['state'] | s1['client']))
out['toy_counts'] = {'state_files': len(s1['state']), 'client_files': len(s1['client'])}
ck('Q9.v_toy_state_set_is_exactly_the_expected_files', len(s1['state']) == 13 and len(s1['client']) == 6, state=len(s1['state']), client=len(s1['client']), expected_state='8 dirs + 1 subdir + users.json + 2 reservas + iald_web/data = 13 (lock excluido)', expected_client='4 arquivos nas arvores + 2 configs = 6 (Pods excluido)')
# --- B2 mutacao de conta / sqlite -wal / arvore de dados / cliente
def mutate_case(path, content, field):
    a = snap()
    Path(path).write_bytes(content)
    b = snap()
    rr = T.scope_compare(a, b)
    return tri(rr), rr
cases = {}
cases['users_json_changed'] = mutate_case(TOY / 'iald_users.json', b'{"users":[1]}', 'accounts')[0]
cases['wal_changed'] = mutate_case(TOY / 'iald_uso_claude.json.reservas.sqlite3-wal', b'wal2', 'accounts')[0]
cases['wallet_subdir_changed'] = mutate_case(TOY / '.iald_runtime/monthly_wallet/sub/ledger.db', b'ledger2', 'accounts')[0]
cases['iald_web_data_changed'] = mutate_case(TOY / 'iald_web/data/users.json', b'{"a":1}', 'accounts')[0]
cases['client_www_changed'] = mutate_case(TOY / 'iald-app/www/app.js', b'console.log(2)', 'client')[0]
cases['client_config_changed'] = mutate_case(TOY / 'iald-app/capacitor.config.json', b'{"a":1}', 'client')[0]
cases['client_android_src_changed'] = mutate_case(TOY / 'iald-app/android/app/src/main/A.java', b'class B{}', 'client')[0]
cases['lock_file_changed_is_ignored'] = mutate_case(TOY / '.iald_runtime/monthly_wallet/web-runtime.lock', b'lock-changed', 'accounts')[0]
cases['pods_dir_changed_is_ignored'] = mutate_case(TOY / 'iald-app/ios/Pods/skipme.txt', b'pods2', 'client')[0]
# arquivo novo / apagado
a = snap(); (TOY / '.iald_runtime/invites/new_invite.json').write_bytes(b'n'); b = snap(); cases['state_file_created'] = tri(T.scope_compare(a, b))
a = snap(); (TOY / '.iald_runtime/invites/new_invite.json').unlink(); b = snap(); cases['state_file_deleted'] = tri(T.scope_compare(a, b))
out['toy_mutation_cases'] = cases
exp = {'users_json_changed': (True, False, False), 'wal_changed': (True, False, False), 'wallet_subdir_changed': (True, False, False), 'iald_web_data_changed': (True, False, False),
       'client_www_changed': (False, False, True), 'client_config_changed': (False, False, True), 'client_android_src_changed': (False, False, True),
       'lock_file_changed_is_ignored': (False, False, False), 'pods_dir_changed_is_ignored': (False, False, False), 'state_file_created': (True, False, False), 'state_file_deleted': (True, False, False)}
ck('Q9.v_toy_mutation_cases_true_where_expected_false_otherwise', cases == exp, got=cases)
make_toy()

# --- B3 listener
base = {'18765': [], '18766': [], '8081': [{'pid': 11, 'create_time': 1.5}]}
def lst_case(before, after):
    LST['cur'] = before; a = snap(); LST['cur'] = after; b = snap()
    return tri(T.scope_compare(a, b))
lc = {}
lc['same_nobody_listening_bench'] = lst_case(base, base)
lc['bench_pid_changed_18765'] = lst_case({**base, '18765': [{'pid': 5, 'create_time': 10.0}]}, {**base, '18765': [{'pid': 6, 'create_time': 20.0}]})
lc['bench_same_pid_same_time'] = lst_case({**base, '18766': [{'pid': 5, 'create_time': 10.0}]}, {**base, '18766': [{'pid': 5, 'create_time': 10.0}]})
lc['bench_pid_reused_new_create_time'] = lst_case({**base, '18766': [{'pid': 5, 'create_time': 10.0}]}, {**base, '18766': [{'pid': 5, 'create_time': 99.0}]})
lc['bench_stopped'] = lst_case({**base, '18765': [{'pid': 5, 'create_time': 10.0}]}, base)
lc['bench_started'] = lst_case(base, {**base, '18765': [{'pid': 5, 'create_time': 10.0}]})
lc['only_local_model_8081_changed'] = lst_case(base, {**base, '8081': [{'pid': 12, 'create_time': 3.0}]})
out['toy_listener_cases'] = lc
ck('Q9.v_toy_listener_cases', lc == {'same_nobody_listening_bench': (False, False, False), 'bench_pid_changed_18765': (False, True, False), 'bench_same_pid_same_time': (False, False, False), 'bench_pid_reused_new_create_time': (False, True, False),
                                    'bench_stopped': (False, True, False), 'bench_started': (False, True, False), 'only_local_model_8081_changed': (False, False, False)}, got=lc)
LST['cur'] = base

# --- B4 leitura impossivel de verdade: arquivo aberto por outro handle SEM compartilhamento (CreateFileW dwShareMode=0)
k32 = ctypes.WinDLL('kernel32', use_last_error=True)
k32.CreateFileW.restype = wintypes.HANDLE
k32.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID, wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
k32.CloseHandle.argtypes = [wintypes.HANDLE]
GENERIC_READ, OPEN_EXISTING, INVALID = 0x80000000, 3, wintypes.HANDLE(-1).value


def lock_exclusive(path):
    h = k32.CreateFileW(str(path), GENERIC_READ, 0, None, OPEN_EXISTING, 0, None)
    if h == INVALID or h is None:
        raise OSError(ctypes.get_last_error(), 'could not lock ' + str(path))
    return h


make_toy()
ul = {}
# (a) legivel antes, bloqueado depois, nada mais mudou -> None (nunca False)
a = snap(); h = lock_exclusive(TOY / 'iald_users.json'); b = snap(); k32.CloseHandle(h)
r = T.scope_compare(a, b); ul['state_unreadable_after_only'] = tri(r); ul['unreadable_listed'] = r['scope_measurement']['state_unreadable']
# (b) bloqueado nos dois -> None
h = lock_exclusive(TOY / 'iald_users.json'); a = snap(); b = snap(); k32.CloseHandle(h); ul['state_unreadable_both'] = tri(T.scope_compare(a, b))
# (c) outro arquivo mudou e este ilegivel -> True (mudanca confirmada num legivel)
a = snap(); (TOY / 'iald-app/www/app.js').write_bytes(b'x'); (TOY / '.iald_runtime/invites/invites.dat').write_bytes(b'changed')
h = lock_exclusive(TOY / 'iald_users.json'); b = snap(); k32.CloseHandle(h); ul['unreadable_plus_real_change'] = tri(T.scope_compare(a, b))
make_toy()
# (d) cliente ilegivel -> client None, accounts False
a = snap(); h = lock_exclusive(TOY / 'iald-app/www/app.js'); b = snap(); k32.CloseHandle(h); ul['client_unreadable'] = tri(T.scope_compare(a, b))
# (e) ilegivel que MUDA para legivel com conteudo diferente (so' um lado erro) -> None, nao True
make_toy()
h = lock_exclusive(TOY / 'iald_users.json'); a = snap(); k32.CloseHandle(h); (TOY / 'iald_users.json').write_bytes(b'{"users":[7]}'); b = snap()
ul['unreadable_before_readable_different_after'] = tri(T.scope_compare(a, b))
out['toy_unreadable_cases'] = ul
ck('Q9.iii_v_real_unreadable_file_is_None_never_False_and_never_a_change', ul['state_unreadable_after_only'] == (None, False, False) and ul['state_unreadable_both'] == (None, False, False) and ul['unreadable_plus_real_change'] == (True, False, True)
   and ul['client_unreadable'] == (False, False, None) and ul['unreadable_before_readable_different_after'] == (None, False, False), got=ul)
make_toy()

# --- B5 falha de GRUPO (injecao): state, client, listeners
orig_walk, orig_files = T._scope_walk, T._scope_files
def boom_walk_for(prefix):
    def w(base):
        if str(base).startswith(prefix):
            raise RuntimeError('injected walk failure')
        return orig_walk(base)
    return w
g = {}
T._scope_walk = boom_walk_for(str(TOY / '.iald_runtime'))
a = snap(); b = snap(); r = T.scope_compare(a, b); g['state_group_fails'] = tri(r); g['errors'] = [e['group'] for e in r['scope_measurement']['errors']]
T._scope_walk = boom_walk_for(str(TOY / 'iald-app'))
a = snap(); b = snap(); g['client_group_fails'] = tri(T.scope_compare(a, b))
T._scope_walk = orig_walk
def bad_listeners(port):
    raise PermissionError('AccessDenied injected')
T._scope_listeners = bad_listeners
a = snap(); b = snap(); r = T.scope_compare(a, b); g['listeners_group_fails'] = tri(r); g['listener_errors'] = [e['group'] for e in r['scope_measurement']['errors']]
T._scope_listeners = lambda port: LST['cur'][str(port)]
# falha de ImportError do psutil (simulada) dentro da funcao real
import builtins
real_import = builtins.__import__
def no_psutil(name, *a, **k):
    if name == 'psutil':
        raise ImportError('psutil missing (injected)')
    return real_import(name, *a, **k)
T._scope_listeners = real_listeners
builtins.__import__ = no_psutil
try:
    a = snap(); b = snap(); g['psutil_missing'] = tri(T.scope_compare(a, b))
finally:
    builtins.__import__ = real_import
T._scope_listeners = lambda port: LST['cur'][str(port)]
# _scope_files com excecao NAO-OSError (ex.: MemoryError simulado) -> grupo falha, nao levanta
T._scope_files = lambda paths: (_ for _ in ()).throw(MemoryError('injected'))
a = snap(); b = snap(); g['hashing_memoryerror'] = tri(T.scope_compare(a, b))
T._scope_files = orig_files
out['toy_group_failure_cases'] = g
ck('Q9.ii_iii_v_group_failures_never_raise_and_become_None', g['state_group_fails'] == (None, False, False) and g['client_group_fails'] == (False, False, None) and g['listeners_group_fails'] == (False, None, False) and g['psutil_missing'] == (False, None, False) and g['hashing_memoryerror'] == (None, False, None), got=g)

# --- B6 chaves ausentes / entradas estranhas em scope_compare e scope_snapshot
weird = {}
def try_cmp(name, x, y):
    try:
        r = T.scope_compare(x, y); weird[name] = tri(r)
    except Exception as e:
        weird[name] = 'RAISED ' + type(e).__name__ + ': ' + str(e)[:80]
try_cmp('empty_both', {}, {})
try_cmp('errors_only', {'errors': []}, {'errors': []})
try_cmp('state_empty_dicts', {'state': {}, 'client': {}, 'listeners': {}}, {'state': {}, 'client': {}, 'listeners': {}})
try_cmp('one_side_missing', {'state': {'k': {'bytes': 1, 'sha256': 'x'}}}, {})
try_cmp('error_entry_without_bytes', {'state': {'k': {'error': 'E'}}}, {'state': {'k': {'error': 'E'}}})
try_cmp('listeners_missing_ports', {'listeners': {'18765': []}}, {'listeners': {}})
try_cmp('plan_overlap_missing', {'state': {'k': {'bytes': 1, 'sha256': 'x'}}, 'client': {'c': {'bytes': 1, 'sha256': 'y'}}, 'listeners': {'18765': [], '18766': [], '8081': []}}, {'state': {'k': {'bytes': 1, 'sha256': 'x'}}, 'client': {'c': {'bytes': 1, 'sha256': 'y'}}, 'listeners': {'18765': [], '18766': [], '8081': []}})
try_cmp('non_ascii_keys', {'state': {'ç/σ': {'bytes': 1, 'sha256': 'x'}}, 'client': {'ç': {'bytes': 1, 'sha256': 'x'}}, 'listeners': {'18765': [], '18766': []}}, {'state': {'ç/σ': {'bytes': 1, 'sha256': 'x'}}, 'client': {'ç': {'bytes': 1, 'sha256': 'x'}}, 'listeners': {'18765': [], '18766': []}})
for nm, dd in (('destinations_empty', []), ('destinations_str_list', [str(TOY / 'a')]), ('destinations_pathlike', [TOY / 'a'])):
    try:
        s = T.scope_snapshot(dd); weird['snapshot_' + nm] = 'ok'
    except Exception as e:
        weird['snapshot_' + nm] = 'RAISED ' + type(e).__name__
for nm, dd in (('destinations_None_item', [None]), ('destinations_int_item', [5])):
    try:
        T.scope_snapshot(dd); weird['snapshot_' + nm] = 'ok'
    except Exception as e:
        weird['snapshot_' + nm] = 'RAISED ' + type(e).__name__ + ' (so' + chr(39) + ' com destino invalido; apply_plan teria falhado ANTES de escrever em Path(item["destination"]))'
out['weird_inputs'] = weird
ck('Q9.ii_missing_keys_and_odd_inputs_do_not_raise_in_scope_compare', all(not str(v).startswith('RAISED') for k, v in weird.items() if not k.startswith('snapshot_destinations_None') and not k.startswith('snapshot_destinations_int')), weird=weird)
# --- B6b nome de arquivo com substituto solitario (surrogate) em arvore medida: pode derrubar scope_compare (UnicodeEncodeError em _scope_aggregate)?
make_toy()
sur = {}
try:
    p = TOY / ('.iald_runtime/invites/bad_' + '\ud800' + '.json')
    p.write_bytes(b'x')
    sur['created_file_with_lone_surrogate_name'] = True
except Exception as e:
    sur['created_file_with_lone_surrogate_name'] = 'could not create: ' + type(e).__name__
if sur.get('created_file_with_lone_surrogate_name') is True:
    try:
        a = T.scope_snapshot(dests); b = T.scope_snapshot(dests)
        sur['snapshot'] = 'ok'
        try:
            r = T.scope_compare(a, b); sur['compare'] = 'ok ' + str(tri(r))
        except Exception as e:
            sur['compare'] = 'RAISED ' + type(e).__name__ + ': ' + str(e)[:100]
    except Exception as e:
        sur['snapshot'] = 'RAISED ' + type(e).__name__
out['lone_surrogate_filename'] = sur
ck('Q9.ii_filename_with_lone_surrogate_in_measured_tree_does_not_make_scope_compare_raise', str(sur.get('compare', '')).startswith('ok') or sur.get('created_file_with_lone_surrogate_name') is not True, gating=False,
   result=sur, severity_judged_by_reviewer='BAIXO: classe de entrada rara; conferida ausente no conjunto medido vivo (scope_compare vivo roda sem excecao); efeito = excecao DEPOIS da escrita, sem deployment.json')
make_toy()

# --- B7 FUZZ diferencial: oraculo independente (escrito por mim) x scope_compare
rng = random.Random(407407)
G = ('state', 'client', 'listeners')
def rand_files(n):
    d = {}
    for i in range(n):
        k = 'f%d' % rng.randrange(8)
        d[k] = {'error': 'E%d' % rng.randrange(2)} if rng.random() < 0.12 else {'bytes': rng.randrange(3), 'sha256': 'h%d' % rng.randrange(3)}
    return d
def rand_listeners():
    if rng.random() < 0.1:
        return {}
    return {p: ([{'pid': rng.randrange(3), 'create_time': float(rng.randrange(2))}] if rng.random() < 0.5 else []) for p in ('18765', '18766', '8081')}
def rand_snap():
    s = {'errors': [{'group': rng.choice(G), 'error': 'x'}] if rng.random() < 0.08 else []}
    s['state'] = rand_files(rng.randrange(0, 5)); s['client'] = rand_files(rng.randrange(0, 5)); s['listeners'] = rand_listeners()
    if rng.random() < 0.1:
        del s[rng.choice(['state', 'client', 'listeners', 'errors'])]
    return s
def oracle_files(before, after, name):
    a, b = before.get(name, {}), after.get(name, {})
    failed = {e['group'] for e in list(before.get('errors', [])) + list(after.get('errors', []))}
    bad = {k for side in (a, b) for k, v in side.items() if 'error' in v}
    changed = any(k not in bad and a.get(k) != b.get(k) for k in set(a) | set(b))
    if changed:
        return True
    return False if (name not in failed and a and b and not bad) else None
def oracle_listeners(before, after):
    failed = {e['group'] for e in list(before.get('errors', [])) + list(after.get('errors', []))}
    la, lb = before.get('listeners', {}), after.get('listeners', {})
    if 'listeners' in failed or not la or not lb:
        return None
    return any(la.get(str(p)) != lb.get(str(p)) for p in (18765, 18766))
n_raise, n_mis, violations = 0, 0, []
dist = {'accounts': {True: 0, False: 0, None: 0}, 'client': {True: 0, False: 0, None: 0}, 'bench': {True: 0, False: 0, None: 0}}
for i in range(20000):
    x, y = rand_snap(), rand_snap()
    if rng.random() < 0.3:   # pares proximos (mais Falsos)
        y = json.loads(json.dumps(x))
        if rng.random() < 0.3 and y.get('state'):
            k = next(iter(y['state'])); y['state'][k] = {'bytes': 9, 'sha256': 'zz'}
    try:
        r = T.scope_compare(x, y)
    except Exception as e:
        n_raise += 1; violations.append(('raise', type(e).__name__)); continue
    got = (r['accounts_modified'], r['bench_restarted'], r['client_files_changed'])
    want = (oracle_files(x, y, 'state'), oracle_listeners(x, y), oracle_files(x, y, 'client'))
    for gi, nm in zip(got, ('accounts', 'bench', 'client')):
        dist[nm][gi] += 1
    if any(type(v) not in (bool, type(None)) for v in got):
        violations.append(('not_tristate', got))
    if got != want:
        n_mis += 1; violations.append(('differs_from_oracle', got, want))
        if len(violations) > 5: break
out['fuzz'] = {'pairs': 20000, 'raised': n_raise, 'differs_from_independent_oracle': n_mis, 'distribution': {k: {str(a): b for a, b in v.items()} for k, v in dist.items()}, 'violations_sample': violations[:3]}
ck('Q9.ii_iii_fuzz_20000_pairs_no_exception_tristate_and_equal_to_independent_oracle', n_raise == 0 and n_mis == 0 and not violations, **{k: v for k, v in out['fuzz'].items() if k != 'violations_sample'})
# invariante pedida: 'None nunca vira False' -> False so' com grupo legivel e nao vazio nos dois lados (testado pelo oraculo acima)

T.ROOT = R   # volta ao vivo para a medicao so' de leitura
shutil.rmtree(TOY, ignore_errors=True)

# ======================================================== D. vivo, so' leitura: eventos de auditoria, tempo, cobertura
events = {}
def hook(event, args):
    if event.startswith(('open', 'os.', 'shutil.', 'subprocess.', 'socket.', 'glob.', 'sqlite3.', 'pathlib.')) and event not in ('os.listdir', 'os.scandir', 'glob.glob'):
        if event == 'open':
            path, mode, flags = args
            if isinstance(path, int):
                return
            key = 'open:' + str(mode) + (':WRITEFLAGS' if (isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC)) else ':ro')
        else:
            key = event
        events[key] = events.get(key, 0) + 1
    elif event in ('os.listdir', 'os.scandir', 'glob.glob'):
        events[event] = events.get(event, 0) + 1
live_plan = json.loads((W / 'install_plan.json').read_bytes())
live_dests = [i['destination'] for i in live_plan['files']]
T.ROOT = R
T._scope_listeners = real_listeners
sys.addaudithook(hook)
live = []
for i in range(3):
    t0 = time.perf_counter(); s = T.scope_snapshot(live_dests); live.append((round(time.perf_counter() - t0, 3), s))
sys.addaudithook(lambda e, a: None)   # (hooks nao podem ser removidos; este so' encerra o registro logico abaixo)
events_final = dict(events)
sa, sb = live[1][1], live[2][1]
rl = T.scope_compare(sa, sb)
out['live'] = {'seconds_each': [x[0] for x in live], 'snapshot_internal_seconds': [x[1]['seconds'] for x in live], 'state_files': len(sa['state']), 'client_files': len(sa['client']), 'errors': sa['errors'], 'plan_overlap': sa['plan_overlap'],
               'tri_between_two_live_snapshots': tri(rl), 'state_bytes': rl['scope_measurement']['state_bytes'], 'client_bytes': rl['scope_measurement']['client_bytes'], 'listeners_8081': sa['listeners'].get('8081'), 'bench_running': {'18765': bool(sa['listeners'].get('18765')), '18766': bool(sa['listeners'].get('18766'))},
               'unreadable_state': rl['scope_measurement']['state_unreadable'], 'unreadable_client': rl['scope_measurement']['client_unreadable'], 'audit_events_3_snapshots': events_final}
write_events = [k for k in events_final if 'WRITEFLAGS' in k or k.startswith(('os.remove', 'os.rename', 'os.mkdir', 'os.rmdir', 'os.chmod', 'os.utime', 'shutil', 'subprocess', 'socket'))]
ck('Q9.i_live_audit_events_show_only_read_only_opens_and_listing', not write_events and set(k for k in events_final if k.startswith('open')) <= {'open:r:ro'}, events=events_final, write_events=write_events, note="o evento 'open' do FileIO reporta o modo cru 'r' (= rb, flags O_RDONLY); o AST confirma que todo open() das funcoes de escopo e' 'rb'")
ck('Q9.vi_live_snapshot_takes_about_0p2_s', max(x[0] for x in live) < 2.0 and 0.05 <= sorted(x[0] for x in live)[1] <= 1.0, seconds=[x[0] for x in live])
ck('Q9.live_two_snapshots_no_errors_all_false', not sa['errors'] and tri(rl) == (False, False, False) and not rl['scope_measurement']['state_unreadable'] and not rl['scope_measurement']['client_unreadable'], tri=tri(rl))
ck('Q9.iv_plan_overlap_live_is_empty', not sa['plan_overlap'])

# ---- cobertura (iv): destinos do plano x conjunto medido (por prefixo) e x candidatos de estado NAO medidos
meas_state = [R / '.iald_runtime' / d for d in T.SCOPE_STATE_DIRS] + [R / 'iald_web/data']
meas_client = [R.joinpath(*t) for t in T.SCOPE_CLIENT_TREES]
under = lambda p, base: Path(p).resolve().is_relative_to(base.resolve())
ov_meas = [d for d in live_dests if any(under(d, b) for b in meas_state + meas_client)] + [d for d in live_dests if Path(d).name in ('iald_users.json',) or Path(d).name.endswith(('.reservas.sqlite3', '.reservas.sqlite3-wal'))]
unmeasured_candidates = {
    'conta_vinculo_do_dono (Apple, DPAPI)': R / 'owner_private',
    'consentimento/privacidade do chat': R / 'owner_private/chat_privacy',
    'carteira_saldo_claude': R / 'iald_saldo_claude.json', 'carteira_saldo_openai': R / 'iald_saldo_openai.json',
    'razao_de_uso_claude': R / 'iald_uso_claude.json', 'razao_de_uso_openai': R / 'iald_uso_openai.json',
    'pedidos_de_acesso (contas)': R / 'iald_pedidos_acesso.json', 'access_requests': R / 'iald_access_requests.json', 'contract_requests': R / 'iald_contract_requests.json',
    'atividade/execucoes de tarefa (task_runs)': R / '.iald_runtime/task_runs', 'artefatos de tarefa (task_artifacts)': R / '.iald_runtime/task_artifacts',
    'estado do sync central': R / 'iald_sync_central_estado.json', 'prazos': R / 'iald_deadlines.json', 'memoria do operador': R / 'iald_memoria.json',
    'cliente web servido (app/)': R / 'app', 'cliente web servido (iald_chat.html)': R / 'iald_chat.html', 'cliente web servido (sw.js)': R / 'sw.js', 'cliente web servido (manifest.json)': R / 'manifest.json', 'cliente web servido (icons/)': R / 'icons',
}
cov = {}
for label, p in unmeasured_candidates.items():
    exists = p.exists()
    n = sum(1 for _ in p.rglob('*') if _.is_file()) if exists and p.is_dir() else (1 if exists else 0)
    inside = any(os.path.normcase(str(q)) in {k for k in sa['state']} | {k for k in sa['client']} for q in ([p] if p.is_file() else []))
    in_meas = False
    if exists:
        pn = os.path.normcase(str(p))
        in_meas = any(k == pn or k.startswith(pn + os.sep) for k in set(sa['state']) | set(sa['client']))
    cov[label] = {'path': str(p.relative_to(R)), 'exists': exists, 'files': n, 'mtime_utc': (time.strftime('%Y-%m-%d', time.gmtime(p.stat().st_mtime)) if exists else None), 'measured_by_v407': in_meas,
                  'plan_writes_inside': any(under(d, p) if p.is_dir() else os.path.normcase(str(d)) == os.path.normcase(str(p)) for d in live_dests)}
out['coverage_candidates'] = cov
out['plan_destinations_inside_measured_set'] = ov_meas
out['plan_destinations_in_unmeasured_candidates'] = [k for k, v in cov.items() if v['plan_writes_inside']]
unmeasured = [k for k, v in cov.items() if v['exists'] and not v['measured_by_v407']]
out['coverage_gaps'] = unmeasured
ck('Q9.iv_no_plan_destination_inside_measured_or_candidate_state_paths', not ov_meas and not out['plan_destinations_in_unmeasured_candidates'], measured_overlap=ov_meas[:3], candidate_overlap=out['plan_destinations_in_unmeasured_candidates'])
ck('Q9.iv_COVERAGE_account_wallet_consent_activity_files_outside_the_measurement', not unmeasured, gating=False, gaps=unmeasured)

json.dump({'out': out, 'checks': chk}, open(HERE / 'q9_transaction_out.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1, default=str)
print(json.dumps({'n_checks': len(chk), 'fails': [c for c in chk if not c['pass']]}, ensure_ascii=False, indent=1, default=str)[:6000])
for k in ('sizes', 'functions', 'Q10_tools_equal_v406', 'toy_mutation_cases', 'toy_listener_cases', 'toy_unreadable_cases', 'toy_group_failure_cases', 'weird_inputs', 'lone_surrogate_filename', 'fuzz', 'live', 'coverage_gaps', 'plan_destinations_in_unmeasured_candidates'):
    print(k, json.dumps(out[k], ensure_ascii=False, default=str)[:1500])
