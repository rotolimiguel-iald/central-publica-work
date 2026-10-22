"""Verify installed public routes without loading the server or calling an AI API."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import unittest
from urllib.request import Request, urlopen

ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
WORK = Path(__file__).parent
sys.dont_write_bytecode = True
sys.path[:0] = [str(ROOT), str(WORK / 'dependencies')]
os.environ['TIKTOKEN_CACHE_DIR'] = str(ROOT / '.iald_runtime/tokenizer_cache')
sys.stdout.reconfigure(encoding='utf-8')

import iald_fontes_publicas as sources

paths = [ROOT / name for name in (
    'iald_fontes_publicas.json', 'iald_fontes_publicas.py',
    'iald_memoria_canonica.py', 'iald_web_server.py')]
before = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
catalog = sources.catalog()
spec = importlib.util.spec_from_file_location(
    'public_index_tests', WORK / 'stage/tests/test_public_sources.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
log = io.StringIO()
result = unittest.TextTestRunner(stream=log, verbosity=2).run(
    unittest.defaultTestLoader.loadTestsFromModule(module))


def check(entry):
    output = {'id': entry['id'], 'url': entry['url']}
    try:
        req = Request(entry['url'], headers={'User-Agent': 'IALD-Public-Index-Check/1.0'})
        with urlopen(req, timeout=20) as response:
            sample = response.read(512)
            output.update(status=response.status, final_url=response.url,
                          sampled_bytes=len(sample))
    except Exception as exc:
        output.update(error=type(exc).__name__)
    return output


with ThreadPoolExecutor(max_workers=5) as pool:
    checks = list(pool.map(check, catalog['entries']))
after = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
report = {
    'checked_at': datetime.now(timezone.utc).isoformat(),
    'scope': 'INSTALLED_MODULE_TESTS_AND_HTTP_PROBES_ONLY_NO_LIVE_MODEL_CALL',
    'source_files_unchanged': before == after,
    'installed_sha256': after,
    'catalog_entries': len(catalog['entries']),
    'tests_run': result.testsRun,
    'tests_passed': result.wasSuccessful(),
    'test_log': log.getvalue(),
    'http_read_scope': '512_BYTES_PER_ENTRY_NOT_FULL_DOCUMENT_VERIFICATION',
    'http_checks': checks,
}
report['status'] = 'PASS' if (before == after and result.wasSuccessful()
    and all(c.get('status') == 200 for c in checks)) else 'FAIL'
target = WORK / ('public_index_verified_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.json')
data = json.dumps(report, ensure_ascii=False, indent=2).encode('utf-8')
temporary = target.with_suffix('.tmp')
with temporary.open('xb') as handle:
    handle.write(data)
assert temporary.read_bytes() == data
temporary.replace(target)
print(json.dumps({'status': report['status'], 'tests_run': result.testsRun,
                  'tests_passed': result.wasSuccessful(),
                  'http_200': sum(c.get('status') == 200 for c in checks),
                  'entries': len(checks), 'report': str(target)}, ensure_ascii=False))
if report['status'] != 'PASS':
    print(log.getvalue())
    print(json.dumps([c for c in checks if c.get('status') != 200], ensure_ascii=False))
    raise SystemExit(1)
