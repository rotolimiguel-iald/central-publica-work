"""Exact-reference receipts for the explicitly authorized organism-memory mission."""
import datetime as dt
import hashlib
import json
import os
import subprocess
import uuid
from pathlib import Path

WORK = Path(__file__).resolve().parent
REFERENCE = WORK / 'SESSION_REFERENCE.json'
ACTOR = {'id': 'codex-gerente-tgl', 'kind': 'agent'}
PYTHON = r'C:\Python314\python.exe'
CORE = Path(r'C:\IALD\MEMORIA_IALD')

def pin(path):
    p = Path(path)
    return {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}

def save(path, value):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')
    temp = p.with_name(p.name + '.tmp_' + uuid.uuid4().hex)
    with temp.open('xb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    assert temp.read_bytes() == raw
    os.rename(temp, p)

def call(cli, payload, label):
    stamp = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
    stem = WORK / 'receipts' / (stamp + '_' + label)
    save(stem.with_suffix('.request.json'), payload)
    cp = subprocess.run([PYTHON, '-B', '-X', 'utf8', str(CORE / cli)],
        input=json.dumps(payload, ensure_ascii=False), capture_output=True, text=True, encoding='utf-8')
    result = json.loads(cp.stdout)
    receipt = stem.with_suffix('.receipt.json')
    save(receipt, result)
    if cp.returncode or not result.get('ok'):
        raise RuntimeError(f'{receipt}: {result.get("error")} {result.get("message")}')
    return result['result'], receipt

def project():
    return call('mission_cli.py', {'operation': 'project', 'reference': str(REFERENCE),
                                 'max_chars': 125000}, 'project')

def check(task_id):
    current, receipt = project()
    task = next(x for x in current['projection']['active'] if x['id'] == task_id)
    result, checked = call('mission_cli.py', {'operation': 'check', 'reference': str(REFERENCE),
        'actor': ACTOR, 'task_id': task_id, 'lease_id': task['lease']['id'],
        'expected_revision': current['receipt']['revision'],
        'projection_sha256': current['projection_sha256']}, 'check_' + task_id)
    return result, checked
