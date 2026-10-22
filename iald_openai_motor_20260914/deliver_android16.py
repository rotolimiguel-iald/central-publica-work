"""Run only after the pending build-16 publication approval is granted."""
import hashlib
import json
from pathlib import Path
import requests
from goal16_records import ROOT, WORK, record, write_new

memory_before = (ROOT / 'CLAUDE.md').read_bytes()
verification = json.loads((WORK / 'android16_verification.json').read_bytes())
audit = json.loads((WORK / 'mobile16_audit.json').read_bytes())
for name, item in audit['files'].items():
    assert hashlib.sha256((ROOT / 'iald-app' / name).read_bytes()).hexdigest() == item['sha256'], name
apk = next(item for item in verification['files'] if item['file'].endswith('.apk'))
data = Path(apk['file']).read_bytes()
assert len(data) == apk['bytes'] and hashlib.sha256(data).hexdigest() == apk['sha256']
target = ROOT / 'downloads/IALD-4.1-16.apk'
write_new(target, data)
assert target.read_bytes() == data
url = 'https://demo.iald.ia.br/downloads/IALD-4.1-16.apk'
with requests.get(url, timeout=20, allow_redirects=False, stream=True) as response:
    status, location = response.status_code, response.headers.get('Location', '')
assert status == 302 and 'login' in location
receipt = record('android16_delivery.json', {
    'task': 'T4 — entrega Android autenticada', 'status': '[REAL]',
    'artifact': apk, 'destination_file': str(target), 'download_url': url,
    'anonymous_http_status': status, 'anonymous_redirect': location,
    'device_installation': 'NOT_TESTED', 'google_play': 'PENDING_DUNS',
}, '[REAL] Após autorização específica da build 16, APK verificado copiado byte a byte '
   'para downloads/IALD-4.1-16.apk; rota HTTPS exige login (302 para /login). '
   'Não equivale a upload no Google Play nem a instalação comprovada.', memory_before)
print(json.dumps({'receipt': str(receipt), 'download_url': url}, ensure_ascii=False))
