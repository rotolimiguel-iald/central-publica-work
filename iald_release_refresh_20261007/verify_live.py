"""Read-only validation of the installed scientific/control release and services."""
from datetime import datetime, timezone
from pathlib import Path
import http.client
import json
import sys

W = Path(__file__).resolve().parent
R = Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path[:0] = [str(R), str(W)]
from transaction import digest, write_evidence, bench_snapshot
from iald_release_binding import load_release
from claude_memory_package import load_package
import iald_jev_control as control
import iald_auto_router as router
import iald_operator_bench as bench


def request(host, path, expected, tls=False):
    connection = (http.client.HTTPSConnection(host, timeout=20) if tls
                  else http.client.HTTPConnection(host, timeout=20))
    try:
        connection.request('GET', path)
        response = connection.getresponse()
        content = response.read(1024 * 1024 + 1)
        if response.status not in expected or len(content) > 1024 * 1024:
            raise ValueError('Unexpected HTTP response: ' + path)
        if response.status == 302 and response.getheader('Location') != '/login':
            raise ValueError('Protected route must redirect only to local login')
        return {'host': host, 'path': path, 'status': response.status,
                'bytes': len(content), 'sha256': digest(content), 'tls': tls,
                'login_redirect': response.status == 302}
    finally:
        connection.close()


def main():
    if (W / 'live_validation.json').exists():
        raise RuntimeError('Existing live validation: inspect it before repeating')
    plan = json.loads((W / 'install_plan.json').read_bytes())
    deployed = json.loads((W / 'deployment.json').read_bytes())
    restarted = json.loads((W / 'restart.json').read_bytes())
    if (deployed['plan_sha256'] != digest((W / 'install_plan.json').read_bytes())
            or restarted['status'] != 'PASS'):
        raise ValueError('Missing installation/restart evidence')
    for item in plan['files']:
        if digest(Path(item['destination']).read_bytes()) != item['sha256']:
            raise ValueError('Installed file differs: ' + Path(item['destination']).name)
    release = load_release(R / 'iald_nucleo_fixo.json')
    if release.identity != plan['release']:
        raise ValueError('Scientific release differs from plan')
    contract = control.load_contract(R)
    if (contract['release'] != release.identity['release']
            or contract['source_sha256'] != release.identity['source_sha256']):
        raise ValueError('Executive control and scientific source differ')
    _, source = router.memory_slice(R)
    if source['release_source_sha256'] != contract['source_sha256']:
        raise ValueError('Router scientific excerpt differs')
    package = load_package(R / '.iald_runtime/haiku', canonical_manifest=R / 'iald_nucleo_fixo.json',
                           source_sha=release.identity['source_sha256'])
    budget = json.loads((R / '.iald_runtime/haiku/manifest.json').read_bytes())['budget']
    if digest(package.prefix.encode()) != digest((W / 'memory_stage/haiku_prefix.md').read_bytes()):
        raise ValueError('Permanent Haiku memory differs')
    if digest((R / 'IALD_Kernel_v5.txt').read_bytes()) != plan['mother_original_sha256']:
        raise ValueError('Original kernel changed')
    users_raw = (R / 'iald_users.json').read_bytes()
    if digest(users_raw) != plan['account_file_sha256']:
        raise ValueError('Account file changed; reconcile independently before declaring preserved')
    users = json.loads(users_raw)
    if [name for name, record in users.items() if bench.is_operator(record, name)] != ['luiz']:
        raise ValueError('Operator authorization differs')
    questions = control.questions(operator_available=False)
    if 'operator_bench' in questions['work_path']['criteria']:
        raise ValueError('Public operator path exposed')
    resident = bench_snapshot()
    if resident != plan['bench_before']:
        raise ValueError('Resident scientific services changed')
    responses = [request('127.0.0.1:8082', '/login', (200,)),
                 request('127.0.0.1:8082', '/api/task-capabilities', (401, 403)),
                 request('127.0.0.1:8082', '/iald_nucleo_fixo.json', (401, 403, 404, 302)),
                 request('demo.iald.ia.br', '/login', (200,), tls=True)]
    report = {'status': 'PASS', 'utc': datetime.now(timezone.utc).isoformat(),
              'release': release.identity, 'installed_files': len(plan['files']),
              'control_schema': contract['schema'], 'native_permanent_tokens': budget['permanent_tokens'],
              'control_and_memory_bound': True, 'account_file_unchanged': True,
              'operator_accounts': ['luiz'], 'public_operator_path': False,
              'original_kernel_unchanged': True, 'bench_after': resident,
              'bench_observed_state_unchanged': True,
              'resident_state_unchanged': True if all(resident[k].get('status')!='UNAVAILABLE' for k in ('gw','cosmos')) else None,
              'resident_ram_verifiable': all(resident[k].get('status')!='UNAVAILABLE' for k in ('gw','cosmos')), 'http': responses,
              'provider_calls': 0, 'bench_operations': 0, 'client_files_changed': False,
              'scope': 'INSTALLED_LOADERS_AND_HTTP; no end-user generation or physical-device test'}
    write_evidence(W / 'live_validation.json', report)
    print(json.dumps({k: report[k] for k in ('status', 'release', 'installed_files',
                     'native_permanent_tokens', 'resident_state_unchanged', 'provider_calls')}))


if __name__ == '__main__':
    main()
