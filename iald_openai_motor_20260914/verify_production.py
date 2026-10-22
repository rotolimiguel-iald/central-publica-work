"""Ephemeral free account; real public HTTPS consent, retrieval and revocation.

No credentials are printed or persisted outside the protected account database.
Cleanup removes only this exact test record, preserving concurrent user changes.
"""
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess
import tempfile
import sys
import requests
from werkzeug.security import generate_password_hash

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
WORK = Path(__file__).parent
SOURCE = Path(r'C:\IALD\projetos_pyhton\IALD')
USERS = SOURCE / 'iald_users.json'
BASE = 'https://demo.iald.ia.br'
stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
name = 'codex_probe_' + secrets.token_hex(8)
password = secrets.token_urlsafe(32)
password_hash = generate_password_hash(password)
report = {'created_at': datetime.now().astimezone().isoformat(), 'base_url': BASE,
          'scope': 'REAL_HTTPS_APP_AUTH_CONSENT_AND_PUBLIC_RETRIEVAL', 'checks': {}}

def protect(path):
    account = subprocess.check_output(['whoami'], text=True).strip()
    subprocess.run(['icacls', str(path), '/inheritance:r', '/grant:r',
                    account + ':(F)', 'SYSTEM:(F)'], check=True, capture_output=True)

def mutate(change, label):
    for attempt in range(3):
        original = USERS.read_bytes()
        records = json.loads(original)
        if not isinstance(records, dict) or not any(x.get('admin') for x in records.values()):
            raise RuntimeError('User database validation failed')
        change(records)
        payload = json.dumps(records, ensure_ascii=False, indent=2).encode('utf-8')
        backup = USERS.with_name(USERS.name + '.bak_' + stamp + '_' + label + '_' + str(attempt))
        backup.touch(exist_ok=False)
        protect(backup)
        backup.write_bytes(original)
        if backup.read_bytes() != original:
            raise RuntimeError('Byte backup differs')
        fd, temporary_name = tempfile.mkstemp(prefix='.users-probe-', dir=SOURCE)
        os.close(fd)
        temporary = Path(temporary_name)
        protect(temporary)
        temporary.write_bytes(payload)
        if temporary.read_bytes() != payload:
            raise RuntimeError('Temporary verification failed')
        if USERS.read_bytes() != original:
            temporary.unlink()
            continue
        os.replace(temporary, USERS)
        if USERS.read_bytes() != payload:
            raise RuntimeError('Concurrent write after replacement')
        return
    raise RuntimeError('Concurrent user updates; no write performed')

def add(records):
    if name in records:
        raise RuntimeError('Unexpected test account collision')
    records[name] = {'admin': False, 'password_hash': password_hash,
                     'motor': 'openai', 'plano': 'gratuito', 'created': datetime.now().isoformat()}

def remove(records):
    current = records.get(name)
    if current is not None and current.get('password_hash') != password_hash:
        raise RuntimeError('Test account identity changed; cleanup refused')
    records.pop(name, None)

def events(response):
    response.encoding = 'utf-8'  # SSE is UTF-8; requests otherwise defaults text/* to Latin-1.
    result = {'status': response.status_code, 'answer': '', 'tools': [], 'warnings': []}
    for line in response.text.splitlines():
        if not line.startswith('data: {'):
            continue
        item = json.loads(line[6:])
        if item.get('iald_status', {}).get('tool'):
            result['tools'].append(item['iald_status']['tool'])
        if item.get('iald_aviso'):
            result['warnings'].append(item['iald_aviso'])
        for choice in item.get('choices', []):
            result['answer'] += choice.get('delta', {}).get('content') or ''
    return result

created = False
try:
    mutate(add, 'create')
    created = True
    session = requests.Session()
    login = session.post(BASE + '/api/entrar/senha', json={'username': name, 'password': password}, timeout=30)
    login.raise_for_status()
    token = login.json()['token']
    session.headers.update({'Authorization': 'Bearer ' + token, 'Origin': 'capacitor://localhost'})
    report['checks']['app_authentication'] = login.status_code == 200
    motor = session.get(BASE + '/api/motor', timeout=30).json()
    report['motor'] = {key: motor.get(key) for key in ('motor', 'modelo', 'disponivel', 'plano')}
    assert motor['motor'] == 'openai' and motor['disponivel'] and not motor['consentimento']['dado']
    message = {'stream': True, 'messages': [{'role': 'user', 'content': 'Explique a relação entre IALD e TGL em uma frase.'}]}
    blocked = events(session.post(BASE + '/v1/chat/completions', json=message, timeout=45))
    report['before_consent'] = blocked
    assert blocked['warnings'] and not blocked['tools']
    consent = session.post(BASE + '/api/motor/consentimento', json={'aceito': True}, timeout=30)
    assert consent.status_code == 200 and consent.json()['consentido']
    report['checks']['consent_recorded'] = True
    message['messages'][0]['content'] = ('Explique em uma frase a relação IALD, TGL, índice e Atlas. '
        'Depois use iald_public_read para ler llms.txt e cite o endereço consultado, diferenciando '
        'o trecho lido dos documentos apenas referenciados. Seja breve.')
    result = events(session.post(BASE + '/v1/chat/completions', json=message, timeout=150))
    report['response'] = result
    assert result['status'] == 200 and result['answer'] and 'iald_public_read' in result['tools']
    assert not result['warnings']
    report['checks']['public_retrieval'] = True
    quota = session.get(BASE + '/api/motor', timeout=30).json()['cota']
    report['quota_after'] = quota
    revoked = session.post(BASE + '/api/motor/consentimento', json={'aceito': False}, timeout=30)
    assert revoked.status_code == 200 and not revoked.json()['consentido']
    blocked_again = events(session.post(BASE + '/v1/chat/completions', json=message, timeout=45))
    assert blocked_again['warnings'] and not blocked_again['tools']
    report['checks']['revocation_blocks_chat'] = True
    report['status'] = 'PASS'
except Exception as exc:
    report['status'] = 'FAIL'
    report['error_type'] = type(exc).__name__
finally:
    if created:
        mutate(remove, 'cleanup')
        report['checks']['ephemeral_account_removed'] = name not in json.loads(USERS.read_bytes())
    target = WORK / ('production_verification_' + stamp + '.json')
    target.write_bytes(json.dumps(report, ensure_ascii=False, indent=2).encode('utf-8'))
    print(json.dumps(report, ensure_ascii=False))
    print('REPORT=' + str(target))
if report['status'] != 'PASS':
    raise SystemExit(1)
