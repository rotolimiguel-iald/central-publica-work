"""Bounded real API probe; never prints the credential or provider error bodies."""
import json
from pathlib import Path
import requests
from dotenv import dotenv_values

key = dotenv_values(r'C:\IALD\projetos_pyhton\IALD\.env').get('IALD_OPENAI_API_KEY')
if not key:
    raise RuntimeError('API key missing')
try:
    response = requests.post('https://api.openai.com/v1/chat/completions',
        headers={'Authorization': 'Bearer ' + key},
        json={'model': 'gpt-4.1-nano', 'messages': [{'role': 'user', 'content': 'Responda somente IALD_API_OK'}],
              'max_completion_tokens': 32, 'store': False}, timeout=(10, 45))
    data = response.json()
    record = {'status': response.status_code, 'model': data.get('model'), 'usage': data.get('usage'),
              'response_ok': any('IALD_API_OK' in c.get('message', {}).get('content', '') for c in data.get('choices', [])),
              'error_code': data.get('error', {}).get('code'), 'error_type': data.get('error', {}).get('type')}
except requests.exceptions.RequestException as error:
    record = {'network_error_type': type(error).__name__, 'credential_printed': False}
target = Path(__file__).with_name('api_probe_result.json')
if target.exists():
    raise RuntimeError('Probe record already exists; preserve it and select a new report name.')
target.write_bytes(json.dumps(record, indent=2).encode('utf-8'))
print(json.dumps(record))
