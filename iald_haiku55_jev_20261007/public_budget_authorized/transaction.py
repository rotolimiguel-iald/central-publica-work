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

ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
WORK = Path(__file__).resolve().parent

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def atomic(path, raw):
    path = Path(path)
    if not raw:
        raise ValueError('Empty deployment file')
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.tmp_v380_' + str(os.getpid()))
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


def apply_plan(plan_path):
    """Apply only a hash-pinned, independently reviewed plan prepared by main."""
    if (WORK/'deployment.json').exists():
        raise RuntimeError('Existing deployment receipt: inspect before continuing')
    plan = json.loads(Path(plan_path).read_bytes())
    validation = json.loads((WORK/'validation/final_checks.json').read_bytes())
    if not validation['passed'] or validation['plan_sha256'] != digest(Path(plan_path).read_bytes()):
        raise ValueError('Validation does not cover deployment plan')
    if not (WORK/'validation/review_final.json').is_file():
        raise ValueError('Independent review missing')
    review = json.loads((WORK/'validation/review_final.json').read_bytes())
    if review['status'] != 'PASS' or review['plan_sha256'] != digest(Path(plan_path).read_bytes()):
        raise ValueError('Independent review differs')
    quiet()
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
            backups[str(dest)] = backup(dest, stamp)
    try:
        for dest, raw in new.items():
            if (dest.read_bytes() if dest.exists() else None) != old[dest]:
                raise RuntimeError('Concurrent edit during deployment')
            if old[dest] != raw:
                written.append(dest)
                atomic(dest, raw)
    except BaseException:
        for dest in reversed(written):
            if old[dest] is not None and dest.read_bytes() == new[dest]:
                atomic(dest, old[dest])
        raise
    report = {'status':'INSTALLED_RESTART_REQUIRED', 'installed_at':datetime.now(timezone.utc).isoformat(),
              'plan_sha256':digest(Path(plan_path).read_bytes()), 'backups':backups,
              'files':{str(p):digest(v) for p,v in new.items()}, 'accounts_modified':False,
              'bench_restarted':False, 'client_files_changed':False}
    write_evidence(WORK/'deployment.json', report)
    return report
