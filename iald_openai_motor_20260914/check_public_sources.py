from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
import requests
import sys
sys.stdout.reconfigure(encoding='utf-8')
root = Path(__file__).parent
entries = json.loads((root / 'stage/iald_fontes_publicas.json').read_bytes())['entries']

def check(entry):
    try:
        with requests.get(entry['url'], stream=True, timeout=(10, 20), allow_redirects=False) as response:
            next(response.iter_content(512), b'')
            return {'id': entry['id'], 'url': entry['url'], 'status': response.status_code,
                    'read_scope': 'HTTP_GET_PROBE_512_BYTES__NOT_FULL_DOCUMENT_READING'}
    except requests.RequestException as error:
        return {'id': entry['id'], 'url': entry['url'], 'error': type(error).__name__}

with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(check, entries))
report = {'checked_at': datetime.now(timezone.utc).isoformat(), 'results': results}
target = root / ('public_sources_http_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.json')
target.write_bytes(json.dumps(report, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps(report, ensure_ascii=False))
print('REPORT=' + str(target))
if any(result.get('status') != 200 for result in results):
    raise SystemExit(1)
