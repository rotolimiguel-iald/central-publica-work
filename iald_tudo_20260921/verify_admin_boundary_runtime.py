"""Read-only production checks; never load the web server or credentials."""
import ast
from datetime import datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest
import urllib.error
import urllib.request

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')

def main():
    spec = importlib.util.spec_from_file_location('boundary_tests', WORK / 'test_admin_only_deadlines.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.STAGE = ROOT
    result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromModule(module))
    assert result.wasSuccessful()

    source = (ROOT / 'iald_web_server.py').read_text(encoding='utf8')
    tree = ast.parse(source)
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == '_alerta_saldo_operador')
    namespace = {}
    exec(compile(ast.Module(body=[node], type_ignores=[]), '<production-alert-function>', 'exec'), namespace)
    assert namespace['_alerta_saldo_operador']({'admin': True}, [], 'luiz') is None

    for client in [ROOT / 'app/iald.js', ROOT / 'iald-app/www/iald.js']:
        text = client.read_text(encoding='utf8')
        for forbidden in ['renderDeadlines', '/api/alertas', 'verificarAlertas', 'operational_deadlines.js']:
            assert forbidden not in text, (client.name, forbidden)

    installed = json.loads((WORK / 'haiku_installed_disabled_20260922_155423_551001.json').read_text(encoding='utf8'))
    hashes = []
    for item in installed['files']:
        path = ROOT / item['relative']
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        hashes.append({'relative': item['relative'], 'sha256': digest, 'matches_install_receipt': digest == item['sha256']})
    assert all(row['matches_install_receipt'] for row in hashes)

    http = []
    for base in ['http://127.0.0.1:8082', 'https://demo.iald.ia.br']:
        for route in ['/health', '/api/alertas', '/admin/api/prazos']:
            request = urllib.request.Request(base + route)
            try:
                with urllib.request.urlopen(request, timeout=20) as response:
                    status = response.status
            except urllib.error.HTTPError as error:
                status = error.code
            http.append({'url': base + route, 'status': status, 'authenticated': False})
        request = urllib.request.Request(base + '/api/contexto', method='OPTIONS', headers={
            'Origin': 'capacitor://localhost',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'X-IALD-Context',
        })
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                status = response.status
                header = response.headers.get('Access-Control-Allow-Headers', '')
        except urllib.error.HTTPError as error:
            status = error.code
            header = error.headers.get('Access-Control-Allow-Headers', '')
        http.append({'url': base + '/api/contexto', 'method': 'OPTIONS', 'status': status,
                     'native_context_header_allowed': 'x-iald-context' in header.lower()})
    assert all(row['status'] == (200 if row['url'].endswith('/health') else 401)
               for row in http if row.get('method') != 'OPTIONS' and row['url'].startswith('http://127.0.0.1:8082'))
    now = datetime.now().astimezone()
    receipt = WORK / ('admin_boundary_runtime_' + now.strftime('%Y%m%d_%H%M%S_%f') + '.json')
    data = {'checked_at': now.isoformat(), 'production_route_tests': result.testsRun,
            'app_and_mobile_have_no_operational_alerts': True,
            'operator_credit_alert_injection_disabled': True,
            'http': http, 'installed_files': hashes,
            'haiku_activation_by_this_check': False, 'paid_requests': 0,
            'limits': 'Local checks passed; public Python requests returned 403, not an authenticated visual test. Device installation not inspected.'}
    with receipt.open('xb') as stream:
        stream.write(json.dumps(data, ensure_ascii=False, indent=2).encode('utf8'))
    print(json.dumps({'receipt': str(receipt), 'tests': result.testsRun, 'files_match': len(hashes), 'http': http}))

if __name__ == '__main__':
    main()
