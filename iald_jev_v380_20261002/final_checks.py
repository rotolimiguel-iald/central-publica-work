"""Close the reviewed plan against existing test receipts and exact staged bytes."""
from datetime import datetime, timezone
from pathlib import Path
import ast
import json

from transaction import digest, write_evidence

W = Path(__file__).resolve().parent
R = Path(r'C:\IALD\projetos_pyhton\IALD')


def read(path):
    return json.loads(Path(path).read_bytes())


def require(condition, label):
    if not condition:
        raise ValueError(label)


def main():
    plan_path = W / 'install_plan.json'
    plan = read(plan_path)
    receipts = {}
    for key, path in {
        'memory': W / 'validation/memory_review.json',
        'integration': W / 'validation/integration_review.json',
        'plan': W / 'validation/plan_review.json',
        'controller': W / 'controller/controller_checks.json',
        'regression': W / 'regression/regression_receipt.json',
        'memory_local': W / 'memory_build/local_validation_20261002_113417_516764.json',
        'provider_budget': sorted((W / 'memory_build').glob('provider_checks_*.json'))[-1],
        'real_decisions': W / 'live_jev_probe.json',
        'native_count': W / 'count_20261002_113914_901730.json',
    }.items():
        receipts[key] = {'path': str(path), 'sha256': digest(path.read_bytes()), 'data': read(path)}
    for key in ('memory', 'integration', 'plan', 'memory_local', 'provider_budget', 'real_decisions'):
        require(receipts[key]['data']['status'] == 'PASS', 'Failed receipt: ' + key)
    controller = receipts['controller']['data']
    require(controller['tests']['status'] == 'PASS' and not controller['tests']['failures']
            and not controller['tests']['errors'], 'Controller tests did not pass')
    for name, item in controller['pins'].items():
        require(digest((W / 'controller' / name).read_bytes()) == item['sha256'], 'Controller evidence changed: ' + name)
    regression = receipts['regression']['data']
    require(regression['integration']['passed'] and not regression['integration']['failures']
            and not regression['integration']['errors'], 'Integration regression failed')
    for name, item in regression['implementation_pins'].items():
        source = W / 'app_patch' / name
        if not source.is_file():
            source = R / name
        require(item['source_matches_tested'] and digest(source.read_bytes()) == item['tested_sha256'],
                'Regression does not cover current source: ' + name)
    for filename, pin in receipts['integration']['data']['input_pins'].items():
        require(digest(Path(filename).read_bytes()) == pin, 'Independent integration review is stale')
    for filename, pin in receipts['provider_budget']['data']['source_pins'].items():
        require(digest(Path(filename).read_bytes()) == pin, 'Budget check is stale')
    require(receipts['plan']['data']['plan_sha256'] == digest(plan_path.read_bytes()), 'Plan review is stale')
    require(receipts['native_count']['data']['budget']['ready'], 'Native count admission failed')
    for item in plan['files']:
        raw = Path(item['source']).read_bytes()
        require(digest(raw) == item['sha256'] and len(raw) == item['bytes'], 'Staged bytes differ')
        if Path(item['destination']).parent == R and Path(item['destination']).suffix == '.py':
            ast.parse(raw)
    require(digest((W / 'app_patch/iald_jev_control.py').read_bytes())
            == digest((W / 'controller/iald_jev_control.py').read_bytes()), 'Controller copy differs')
    require(receipts['native_count']['data']['draft_sha256']
            == digest((W / 'memory_stage/haiku_prefix.md').read_bytes()), 'Native count prefix differs')
    for filename in ('verify_live.py', 'record_delivery.py', 'transaction.py', 'prepare_install.py'):
        ast.parse((W / filename).read_bytes())
    suites = {'controller': controller['tests']['run'],
              'router': receipts['integration']['data']['existing_suites_independently_rerun']['router']['passed'],
              'independent_integration': receipts['integration']['data']['tests'],
              'existing_app_regression': regression['integration']['run'],
              'memory_integration': receipts['memory_local']['data']['tests'],
              'provider_budget': receipts['provider_budget']['data']['tests']}
    report = {'passed': True, 'utc': datetime.now(timezone.utc).isoformat(),
              'plan_sha256': digest(plan_path.read_bytes()), 'installed_file_count': len(plan['files']),
              'test_suites': suites, 'total_tests': sum(suites.values()),
              'scientific_review': receipts['memory']['data']['status'],
              'receipts': {key: {k: value[k] for k in ('path', 'sha256')} for key, value in receipts.items()},
              'real_decision_cases': len(receipts['real_decisions']['data']['cases']),
              'estimated_decision_cost_usd': receipts['real_decisions']['data']['estimated_actual_usd'],
              'client_files_changed': False,
              'operational_scripts': {name: digest((W / name).read_bytes()) for name in
                 ('transaction.py', 'prepare_install.py', 'restart_web.ps1', 'verify_live.py', 'record_delivery.py')}}
    write_evidence(W / 'validation/final_checks.json', report)
    print(json.dumps({k: report[k] for k in ('passed', 'plan_sha256', 'total_tests', 'test_suites')}))


if __name__ == '__main__':
    main()
