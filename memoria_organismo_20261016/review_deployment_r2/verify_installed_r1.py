"""Read-only independent installed-file and receipt verification; no service calls."""
from datetime import datetime, timezone
import json
import sys
from pathlib import Path
import psutil

WORK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORK))
import mission_io as io

def read(name):
    return json.loads((WORK/name).read_bytes())

def verify(pin):
    assert io.pin(pin['path'])['sha256'] == pin['sha256'], pin['path']

plan = read('deployment_r2/INSTALL_PLAN_R1.json')
review = read('deployment_r2/REVIEW_R1.json')
activation = read('deployment_r2/ACTIVATION_R1.json')
final = read('deployment_r2/runs/activation_r1/FINAL_STATE.json')
restart = read('deployment_r2/runs/activation_r1/RESTART.json')
installed = read('live_validation/INSTALLED_R1.json')
assert activation['installation'] == final and activation['restart'] == restart
assert final['status'] == 'INSTALLED' and restart['status'] == 'PASS'
assert io.pin(WORK/'deployment_r2/INSTALL_PLAN_R1.json')['sha256'] == final['plan_sha256'] == review['plan_sha256']
assert io.pin(WORK/'deployment_r2/transaction.py')['sha256'] == review['installer_sha256']
for name, sha in review['deployment_files'].items():
    assert io.pin(WORK/'deployment_r2'/name)['sha256'] == sha
assert len(plan['files']) == len(final['files']) == len(installed['files']) == 31
backup_pins = []
for index, (planned, actual) in enumerate(zip(plan['files'], final['files'])):
    for field in ('source', 'destination', 'sha256', 'baseline'):
        assert planned[field] == actual[field]
    verify({'path':actual['source'], 'sha256':actual['sha256']})
    verify({'path':actual['destination'], 'sha256':actual['sha256']})
    for stage in ('prepared', 'intent', 'installed'):
        assert read(f'deployment_r2/runs/activation_r1/{index:04d}_{stage}.json') == actual
    if actual['baseline'] is None:
        assert actual['backup'] is None
    else:
        pin = io.pin(actual['backup']); assert pin['sha256'] == actual['baseline']
        backup_pins.append(pin)
        if 'backup_directory' in planned:
            assert Path(actual['backup']).parent == Path(planned['backup_directory'])
        else:
            assert Path(actual['backup']).parent == Path(actual['destination']).parent
for pin in installed['files'] + installed['new_process_imports']:
    verify(pin)
verify(installed['restart'])
parent = psutil.Process(restart['supervisor_pid'])
web = psutil.Process(restart['new_web_pid'])
assert parent.create_time() == restart['supervisor_created']
assert web.ppid() == parent.pid
assert any(str(x).lower().endswith('iald_web_server.py') for x in web.cmdline())
assert web.create_time() >= datetime.fromisoformat(final['started_utc']).timestamp()
process = {'supervisor_pid':parent.pid, 'supervisor_created':parent.create_time(),
           'web_pid':web.pid, 'web_created':web.create_time(), 'web_parent_pid':web.ppid(),
           'web_status':web.status(), 'script_path_matches':True,
           'new_http_request_made_by_reviewer':False}

jev = read('live_validation/jev_long/RESULT_R1.json')
assert jev['status']=='PASS' and jev['http_status']==200 and jev['calls']==1
assert jev['admission']['context_mode']=='long'
assert jev['outcome']['accepted'] is False and jev['outcome']['terminal'] is True
verify(jev['outcome']['ticket']['source'])
mcp = read('live_validation/MCP_INSTALLED_R1.json')
assert mcp['status']=='PASS' and mcp['exit']==0 and mcp['tool_count']==20
assert len(mcp['new_tools'])==7 and mcp['tool_calls']==0
verify(mcp['source'])
bench = read('live_validation/BENCH_GET_R1.json')
connect = read('live_validation/BENCH_CONNECTIVITY_R1.json')
assert bench['repeated'] is False and connect['previous_request_repeated'] is False
assert connect['status']=='UNAVAILABLE' and connect['connect_ex']==10061
handles = bench['recovery']['activity']['handles']
assert any(x['status']=='uncertain' and x['no_repeat'] for x in handles)
verify(bench['recovery']['activity']['ticket']['source'])

projection, receipt = io.project()
result = {'status':'PASS_INSTALLED_COMPONENTS_WITH_OPEN_D', 'review_complete':False,
          'requirement_satisfied':False, 'author':'codex-organism-deployment-review',
          'time_utc':datetime.now(timezone.utc).isoformat(), 'revision':projection['receipt']['revision'],
          'reference':str(WORK/'SESSION_REFERENCE.json'), 'projection':io.pin(receipt),
          'observed':{'current_installed_sources':31,'verified_backups':len(backup_pins),
                      'prepared_intent_installed_receipts':93, 'new_process_import_pins':14,
                      'mobile_assets_installed':3,'provider_calls_by_reviewer':0,
                      'web_process_started_by_reviewer':False},
          'process':process, 'backup_pins':backup_pins,
          'evidence':[io.pin(WORK/p) for p in (
              'deployment_r2/ACTIVATION_R1.json','deployment_r2/runs/activation_r1/FINAL_STATE.json',
              'deployment_r2/runs/activation_r1/RESTART.json','live_validation/INSTALLED_R1.json',
              'live_validation/jev_long/RESULT_R1.json','live_validation/MCP_INSTALLED_R1.json',
              'live_validation/BENCH_GET_R1.json','live_validation/BENCH_CONNECTIVITY_R1.json')],
          'material_findings':[],
          'limits':['Aguardando DELIVERY_D_R1 para revisão integral e eventual aceite de D.',
                    'Imports em processo separado não demonstram todas as rotas do web; recibo instalado ainda indica PENDING_AUTHENTICATED_ACTIVITY_HTTP.',
                    'JEV é chamada real pública/sintética em store privado; não é conversa autenticada de ponta a ponta. Retorno candidate, sem aceite semântico.',
                    'MCP comprova descoberta em processo novo; nenhum tool call neste recibo nem recarga dos processos antigos.',
                    'Bancada indisponível: URLError e conexão recusada18777; operação uncertain custodiada, sem repetição. Não é teste científico concluído.',
                    'Três assets móveis copiados; compilação/distribuição e instalação física não demonstradas por estes recibos.'],
          'script':io.pin(__file__)}
io.save(WORK/'review_deployment_r2/INSTALLED_PRECHECK_R1.json',result)
print(json.dumps({'result':io.pin(WORK/'review_deployment_r2/INSTALLED_PRECHECK_R1.json'),
                  'observed':result['observed'],'revision':result['revision']},ensure_ascii=False))
