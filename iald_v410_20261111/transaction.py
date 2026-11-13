"""Audited server deployment primitives; no services or model calls at import."""
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
import ast
import hashlib
import http.client
import json
import os
import sqlite3
import subprocess
import sys
import time

ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
WORK = Path(__file__).resolve().parent

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def atomic(path, raw):
    path = Path(path)
    if not raw:
        raise ValueError('Empty deployment file')
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.tmp_release_' + str(os.getpid()))
    with temp.open('xb') as out:
        out.write(raw)
        out.flush()
        os.fsync(out.fileno())
    if temp.read_bytes() != raw:
        raise ValueError('Temporary file verification failed')
    os.replace(temp, path)
    if path.read_bytes() != raw:
        raise ValueError('Installed file verification failed')

def backup(path, stamp=None):
    path = Path(path)
    raw = path.read_bytes()
    dest = path.with_name(path.name + '.bak_' + (stamp or datetime.now().strftime('%Y%m%d_%H%M%S_%f')))
    with dest.open('xb') as out:
        out.write(raw)
        out.flush()
        os.fsync(out.fileno())
    if dest.read_bytes() != raw:
        raise ValueError('Backup differs from original bytes')
    return str(dest)

def write_evidence(path, value):
    path = Path(path)
    raw = json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False).encode()
    if path.exists():
        if path.read_bytes() == raw:
            return
        backup(path)
    atomic(path, raw)

def quiet():
    jobs = ROOT / '.iald_runtime/chat_jobs/jobs.sqlite3'
    if not jobs.is_file():
        raise ValueError('Missing job ledger')
    paths = [(jobs, "SELECT COUNT(*) FROM jobs WHERE status IN ('queued','running')")]
    paths += [(p, "SELECT COUNT(*) FROM calls WHERE status='reserved'") for p in
              [*ROOT.glob('*.reservas.sqlite3'), ROOT / '.iald_runtime/app_evaluation/public_spend.sqlite3'] if p.is_file()]
    wallet = ROOT / '.iald_runtime/monthly_wallet/wallet.sqlite3'
    if wallet.is_file():
        paths += [(wallet, "SELECT COUNT(*) FROM tasks WHERE status='active'"), (wallet, "SELECT COUNT(*) FROM calls WHERE status='pending'")]
    for path, query in paths:
        with closing(sqlite3.connect(path.as_uri()+'?mode=ro', uri=True)) as db:
            if db.execute(query).fetchone()[0]:
                raise RuntimeError('Active work: do not restart or switch memory')
    return {'active_jobs': 0, 'reserved_calls': 0}

def local_json(port, path):
    conn = http.client.HTTPConnection('127.0.0.1', port, timeout=20)
    try:
        conn.request('GET', path)
        response = conn.getresponse()
        raw = response.read(4 * 1024**2 + 1)
        if response.status != 200 or len(raw) > 4 * 1024**2:
            raise ValueError('Local service failed')
        return json.loads(raw)
    finally:
        conn.close()

def bench_snapshot():
    def observe(port,path):
        try:return local_json(port,path),None
        except ConnectionRefusedError:
            return None,{'status':'UNAVAILABLE','reason':'CONNECTION_REFUSED','port':port,'resident_state_verified':False}
    gw,gw_error=observe(18765,'/api/universe/status')
    co,co_error=observe(18766,'/api/cosmology/status')
    if gw is not None:
        series=sorted((row['id'],row['strain_array_sha256']) for row in gw.get('series',[]))
        g={key:gw.get(key) for key in ('status','domain','load_id','generation','loaded_files','total_files','resident_bytes','worker_pid','errors')}
        arrays=digest(json.dumps(series,sort_keys=True).encode())
    else:g=gw_error;arrays=None
    if co is not None:
        cosmology={**{key:co.get(key) for key in ('status','engine_generation')},**{key:co.get('memory',{}).get(key) for key in ('load_id','loaded_source_bytes','source_reads_total')}}
    else:cosmology=co_error
    return {'gw':g,'strain_arrays_sha256':arrays,'cosmos':cosmology}


# --- v407: escopo da instalacao MEDIDO. Na v406, accounts_modified, bench_restarted e client_files_changed eram constantes False deste arquivo (licao 5 da v406).
# Aqui sao medicoes SOMENTE LEITURA, antes e depois da escrita, dentro da janela com o web parado. Falha de leitura vira None (nao medido), nunca False.
SCOPE_STATE_DIRS = ('app_evaluation', 'app_routing', 'chat_jobs', 'invites', 'monthly_wallet', 'native_push', 'private_media', 'research')   # sob .iald_runtime
SCOPE_STATE_FILES = ('iald_users.json',)
SCOPE_STATE_GLOBS = ('*.reservas.sqlite3', '*.reservas.sqlite3-wal', '*.reservas.sqlite3-shm', '*.reservas.sqlite3-journal')
SCOPE_STATE_TREES = (('iald_web', 'data'),)
SCOPE_CLIENT_TREES = (('app',), ('iald-app', 'www'), ('iald-app', 'ios'), ('iald-app', 'android', 'app', 'src'), ('iald_web', 'app'))
SCOPE_CLIENT_FILES = (('iald-app', 'capacitor.config.json'), ('iald-app', 'package.json'), ('iald-app', 'index.html'),
                      ('iald-app', 'android', 'build.gradle'), ('iald-app', 'android', 'app', 'build.gradle'))
SCOPE_SKIP_DIRS = frozenset(('Pods', 'build', 'DerivedData', 'xcuserdata', '.gradle', '__pycache__', 'node_modules', '.git'))
SCOPE_SKIP_SUFFIXES = ('.lock',)   # travas de processo (ex.: web-runtime.lock, presa pelo web vivo): nao sao dado de usuario
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
            if name.lower().endswith(SCOPE_SKIP_SUFFIXES):
                continue
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
        h.update((key + '\t' + str(v.get('bytes')) + '\t' + str(v.get('sha256') or v.get('error')) + '\n').encode('utf-8', 'surrogatepass'))
    return h.hexdigest()


def scope_compare(before, after):
    errors = list(before.get('errors', [])) + list(after.get('errors', []))
    failed = {e['group'] for e in errors}

    def group(name):
        a, b = before.get(name, {}), after.get(name, {})
        bad = {k for side in (a, b) for k, v in side.items() if 'error' in v}
        unreadable = sorted(bad)
        changed = sorted(k for k in set(a) | set(b) if k not in bad and a.get(k) != b.get(k))   # ilegivel num dos lados = nao medido, nao mudanca
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
            'method': 'sha256 de cada arquivo (estado e cliente; travas *.lock excluidas) e pid+create_time de quem escuta as portas, antes e depois da escrita, dentro da janela com o web parado; somente leitura',
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


def check_science_destinations(files):
    """Accept a new release directory and the eight exact activation files only."""
    from release_cfg import load
    cfg = load(require_commit=True)
    root = ROOT.resolve(strict=True)
    version_dir = root / 'canonical_releases' / cfg.target_name
    manifest = root / 'iald_nucleo_fixo.json'
    fixed = {manifest, root / ('core_packet_' + cfg.release + '_bound.txt')}
    for package in ('haiku', 'haiku55'):
        for filename in ('prefix.md', 'manifest.json', 'native_count.json'):
            fixed.add(root / '.iald_runtime' / package / filename)
    from preservation_guard import runtime_delta
    delta = runtime_delta()
    seen = set()
    for row in files:
        path = Path(row['destination'])
        dest = path.resolve()
        if path != dest or dest in seen:
            raise ValueError('Aliased or duplicate destination in scientific plan')
        if dest in delta and any(row.get(key) != delta[dest].get(key) for key in ('source','destination','sha256','baseline')):
            raise ValueError('Runtime plan differs from reviewed delta')
        if dest not in fixed and dest not in delta and not dest.is_relative_to(version_dir):
            raise ValueError('Destination outside the scientific release')
        if dest.is_relative_to(version_dir) and row['baseline'] is not None:
            raise ValueError('Existing immutable release would be changed')
        seen.add(dest)
    if not (fixed | set(delta)).issubset(seen) or Path(files[-1]['destination']) != manifest:
        raise ValueError('Incomplete scientific activation plan')


def apply_plan(plan_path):
    """Apply only a hash-pinned, independently reviewed plan prepared by main."""
    from maintenance import assert_quiesced
    assert_quiesced()
    if (WORK/'deployment.json').exists():
        raise RuntimeError('Existing deployment receipt: inspect before continuing')
    plan_bytes = Path(plan_path).read_bytes()
    plan_sha256 = digest(plan_bytes)
    plan = json.loads(plan_bytes)
    validation = json.loads((WORK/'validation/final_checks.json').read_bytes())
    if not validation['passed'] or validation['plan_sha256'] != plan_sha256:
        raise ValueError('Validation does not cover deployment plan')
    if not (WORK/'validation/review_final.json').is_file():
        raise ValueError('Independent review missing')
    review = json.loads((WORK/'validation/review_final.json').read_bytes())
    if review['status'] != 'PASS' or review['plan_sha256'] != plan_sha256:
        raise ValueError('Independent review differs')
    check_science_destinations(plan['files'])
    quiet()
    plan_dests = [i['destination'] for i in plan['files']]
    scope_before = scope_snapshot(plan_dests)   # v407: medido dentro da janela, antes de escrever
    if scope_before['plan_overlap']:
        raise ValueError('Release would overwrite protected application state')
    old, new, backups, written = {}, {}, {}, []
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    for item in plan['files']:
        source, dest = Path(item['source']).resolve(), Path(item['destination']).resolve()
        if not source.is_relative_to(WORK) or not dest.is_relative_to(ROOT):
            raise ValueError('Destination outside release scope')
        raw = source.read_bytes()
        prior = dest.read_bytes() if dest.exists() else None
        if digest(raw) != item['sha256'] or (digest(prior) if prior is not None else None) != item['baseline']:
            raise ValueError('Concurrent edit or changed stage: '+dest.name)
        if dest.suffix == '.py' and dest.parent == ROOT:
            ast.parse(raw)
        old[dest], new[dest] = prior, raw
    for dest, prior in old.items():
        if prior is not None and prior != new[dest]:
            if dest.is_relative_to(ROOT / 'iald-app'):
                # Keep raw-byte mobile backups out of bundled assets, as in the
                # established mobile preparer. Memory backups remain in place.
                saved = WORK / 'mobile_backups' / dest.relative_to(ROOT / 'iald-app')
                saved = saved.with_name(saved.name + '.bak_' + stamp)
                saved.parent.mkdir(parents=True, exist_ok=True)
                with saved.open('xb') as out:
                    out.write(prior); out.flush(); os.fsync(out.fileno())
                if saved.read_bytes() != prior:
                    raise OSError('Mobile backup mismatch')
                backups[str(dest)] = str(saved)
            else:
                backups[str(dest)] = backup(dest, stamp)
    try:
        assert_quiesced()
        for dest, raw in new.items():
            if (dest.read_bytes() if dest.exists() else None) != old[dest]:
                raise RuntimeError('Concurrent edit during deployment')
            if old[dest] != raw:
                written.append(dest)
                atomic(dest, raw)
        assert_quiesced()
        # Verify installed loaders in a new offline process before resuming service.
        # Any failure enters the same byte-preserving rollback as an install failure.
        loaded = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(WORK/'verify_installed.py'), '--preflight'],
                                capture_output=True, text=True, encoding='utf-8', timeout=120)
        if loaded.returncode != 0:
            write_evidence(WORK/'LOADER_VERIFICATION_FAILURE.json',
                           {'returncode':loaded.returncode,'stderr':loaded.stderr[-12000:]})
            raise RuntimeError('Installed loader verification failed; rolling back')
        result = json.loads(loaded.stdout)
        if result.get('status') != 'PASS':
            raise RuntimeError('Installed loader verification did not pass')
        assert_quiesced()
    except BaseException:
        for dest in reversed(written):
            if not dest.exists() or dest.read_bytes() != new[dest]:
                continue  # Never overwrite a concurrent writer's change.
            if old[dest] is not None:
                atomic(dest, old[dest])
            else:
                # Restore absence, but retain our newly created bytes as an
                # audit artifact. Both absolute paths are checked before moving.
                source = dest.resolve()
                retained = (WORK / 'rollback_new_files' / stamp /
                            source.relative_to(ROOT.resolve())).resolve()
                if not source.is_relative_to(ROOT.resolve()) or not retained.is_relative_to(WORK.resolve()):
                    raise RuntimeError('Rollback path outside scope')
                retained.parent.mkdir(parents=True, exist_ok=True)
                if retained.exists():
                    raise RuntimeError('Rollback artifact already exists')
                os.replace(source, retained)
        raise
    scope = scope_compare(scope_before, scope_snapshot(plan_dests))   # v407: medido de novo, ainda dentro da janela, depois de escrever
    report = {'status':'INSTALLED_RESTART_REQUIRED', 'installed_at':datetime.now(timezone.utc).isoformat(),
              'plan_sha256':plan_sha256, 'backups':backups,
              'files':{str(p):digest(v) for p,v in new.items()},
              'accounts_modified':scope['accounts_modified'], 'bench_restarted':scope['bench_restarted'],
              'client_files_changed':scope['client_files_changed'], 'scope_measurement':scope['scope_measurement']}
    write_evidence(WORK/'deployment.json', report)
    return report
