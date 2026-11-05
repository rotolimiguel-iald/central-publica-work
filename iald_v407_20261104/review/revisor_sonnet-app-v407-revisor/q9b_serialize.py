"""Revisor sonnet-app-v407-revisor -- Q9 extra: o relatorio com scope_measurement sobrevive a write_evidence? (json.dumps(..., ensure_ascii=False, indent=2, allow_nan=False).encode()).
write_evidence e' chamado DEPOIS da escrita do plano; se falhasse, o plano ficaria instalado sem deployment.json. Testa com snapshots VIVOS (so' leitura) e com casos de brinquedo (None, erro, ilegivel).
Nao chama apply_plan, nao escreve deployment.json (so' serializa em memoria)."""
import importlib.util, json, os, sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
W = Path(r'C:\IALD\Central de Patentes\work\iald_v407_20261104')
def guard(event, args):
    if event in ('socket.connect', 'socket.getaddrinfo', 'subprocess.Popen', 'os.system'):
        raise RuntimeError('blocked ' + event)
    if event == 'open':
        path, mode, flags = args
        if isinstance(path, int):
            return
        p = Path(os.fsdecode(path)).resolve()
        writing = (isinstance(mode, str) and any(c in mode for c in 'wax+')) or (isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC))
        if writing and not p.is_relative_to(HERE):
            raise RuntimeError('write outside reviewer folder: ' + str(p))
sys.addaudithook(guard)
spec = importlib.util.spec_from_file_location('transaction_rev2', W / 'transaction.py')
T = importlib.util.module_from_spec(spec); spec.loader.exec_module(T)
plan = json.loads((W / 'install_plan.json').read_bytes())
dests = [i['destination'] for i in plan['files']]
a = T.scope_snapshot(dests); b = T.scope_snapshot(dests)
r = T.scope_compare(a, b)
report = {'status': 'INSTALLED_RESTART_REQUIRED', 'installed_at': '2026-11-04T00:00:00+00:00', 'plan_sha256': 'x', 'backups': {}, 'files': {},
          'accounts_modified': r['accounts_modified'], 'bench_restarted': r['bench_restarted'], 'client_files_changed': r['client_files_changed'], 'scope_measurement': r['scope_measurement']}
res = {}
raw = json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False).encode()
res['live_report_json_bytes'] = len(raw)
res['live_tri_state'] = [r['accounts_modified'], r['bench_restarted'], r['client_files_changed']]
res['live_keys_of_scope_measurement'] = sorted(r['scope_measurement'])
# caso None (nao medido) tambem serializa
x = {'state': {}, 'client': {}, 'listeners': {}, 'errors': [{'group': 'state', 'error': 'E'}], 'plan_overlap': [], 'seconds': 0.0}
rn = T.scope_compare(x, x)
raw2 = json.dumps({'accounts_modified': rn['accounts_modified'], 'bench_restarted': rn['bench_restarted'], 'client_files_changed': rn['client_files_changed'], 'scope_measurement': rn['scope_measurement']}, ensure_ascii=False, indent=2, allow_nan=False).encode()
res['none_report_json_bytes'] = len(raw2)
res['none_tri_state'] = [rn['accounts_modified'], rn['bench_restarted'], rn['client_files_changed']]
res['serializes_ok'] = True
json.dump(res, open(HERE / 'q9b_serialize_out.json', 'w', encoding='utf8'), indent=1)
print(json.dumps(res, indent=1))
