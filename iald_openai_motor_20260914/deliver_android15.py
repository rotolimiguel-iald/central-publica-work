from pathlib import Path
import hashlib
import json
from datetime import datetime
import requests

WORK = Path(__file__).parent
root = Path(r'C:\IALD\projetos_pyhton\IALD\downloads')
source = WORK / 'artifacts/IALD-4.1-15.apk'
data = source.read_bytes()
metadata = json.loads((WORK / 'android15_verification.json').read_bytes())['files'][0]
assert hashlib.sha256(data).hexdigest() == metadata['sha256']
root.mkdir(exist_ok=True)
target = root / source.name
assert not target.exists(), 'Existing delivery is not overwritten'
temporary = target.with_suffix('.tmp')
temporary.write_bytes(data)
assert temporary.read_bytes() == data
temporary.replace(target)
url = 'https://demo.iald.ia.br/downloads/' + source.name
response = requests.get(url, allow_redirects=False, timeout=20)
assert response.status_code == 302 and '/login' in response.headers.get('Location', ''), 'Authentication gate unexpected'
receipt = {'created_at': datetime.now().astimezone().isoformat(), 'url': url, 'file': str(target),
           'sha256': hashlib.sha256(target.read_bytes()).hexdigest(), 'bytes': len(data),
           'anonymous_status': response.status_code, 'access': 'EXISTING_AUTHENTICATED_DOWNLOAD_ROUTE',
           'phone_download_or_installation': 'NOT_VERIFIED'}
(WORK / 'android15_delivery.json').write_bytes(json.dumps(receipt, indent=2).encode())
print(json.dumps(receipt))
