"""Receipts and exact-reference operations for the authenticated app follow-up."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys
import uuid

ROOT = Path(__file__).resolve().parent
REFERENCE = ROOT.parent / 'SESSION_REFERENCE.json'
CORE = Path(r'C:\IALD\MEMORIA_IALD')
ACTOR = {'id': 'codex-gerente-tgl', 'kind': 'agent'}

def new(name, value):
    p = ROOT / name
    p.parent.mkdir(parents=True, exist_ok=True)
    raw = value if isinstance(value, bytes) else ((value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8'))
    if p.exists():
        raise FileExistsError(p)
    tmp = p.with_name(p.name + '.tmp_' + uuid.uuid4().hex)
    with tmp.open('xb') as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    assert tmp.read_bytes() == raw
    tmp.rename(p)
    return p

def pin(p):
    p = Path(p).resolve()
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}

def call(cli, request, label):
    stamp = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
    prefix = 'receipts/' + label + '_' + stamp
    new(prefix + '_REQUEST.json', request)
    p = subprocess.run([sys.executable, '-B', '-X', 'utf8', str(CORE / cli)], input=json.dumps(request, ensure_ascii=False), capture_output=True, encoding='utf-8')
    result = json.loads(p.stdout)
    out = new(prefix + '_RESULT.json', {'exit_code': p.returncode, 'response': result, 'stderr': p.stderr})
    if p.returncode or not result.get('ok'):
        raise RuntimeError(str(out))
    return result['result'], out

def project():
    return call('mission_cli.py', {'operation': 'project', 'reference': str(REFERENCE), 'max_chars': 400000}, 'PROJECT')[0]

def action(operation, event_id, **extra):
    p = project()
    return call('mission_cli.py', dict(operation=operation, reference=str(REFERENCE), actor=ACTOR, expected_revision=p['receipt']['revision'], projection_sha256=p['projection_sha256'], event_id=event_id, **extra), operation.upper())

def check(task_id):
    p = project()
    task = next(t for t in p['projection']['active'] if t['id'] == task_id)
    return call('mission_cli.py', dict(operation='check', reference=str(REFERENCE), actor=ACTOR, expected_revision=p['receipt']['revision'], projection_sha256=p['projection_sha256'], task_id=task_id, lease_id=task['lease']['id']), 'PREFLIGHT')
