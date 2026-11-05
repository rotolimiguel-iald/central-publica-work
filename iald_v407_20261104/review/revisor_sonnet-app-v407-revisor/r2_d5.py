"""Revisor sonnet-app-v407-revisor -- RODADA 2: D5 (processos). Somente leitura (psutil); unica rede: GET http://127.0.0.1:8082/login.
ADAPTADO de check_d5.py do revisor da v406 (-d): ids e horarios da v407; acrescenta o cruzamento com o log do supervisor e com scope_measurement.listeners_*."""
import http.client, json, sys, time
from datetime import datetime
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import r2lib as L
L.install_guard()
import psutil
W, R, HERE = L.W, L.R, L.HERE
rd = L.rd
rs, mt, dep = rd(W / 'restart.json'), rd(W / 'maintenance.json'), rd(W / 'deployment.json')
sm = dep['scope_measurement']
installed_at = datetime.fromisoformat(dep['installed_at']).timestamp()
fmt = lambda t: datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
def scripts(p):
    try:
        return [Path(a).name for a in p.cmdline()[1:] if a and not a.startswith('-')][:3]
    except Exception as e:
        return ['ERRO:' + type(e).__name__]
def flags(p):
    try:
        return [a for a in p.cmdline()[1:] if a.startswith('-')][:6]
    except Exception as e:
        return ['ERRO:' + type(e).__name__]
old, new, sup = rs['old_web_pid'], rs['new_web_pid'], rs['supervisor_pid']
c = {}
ident = lambda d: {k: d[k] for k in ('old_web_pid', 'supervisor_pid', 'supervisor_created')}
c['maintenance_json_identidade_igual_restart_json'] = ident(mt) == ident(rs)
c['restart_json'] = {k: rs[k] for k in ('status', 'http_status', 'old_web_pid', 'new_web_pid', 'supervisor_pid')}
c['pid_antigo_existe'] = psutil.pid_exists(old)
if c['pid_antigo_existe']:
    po = psutil.Process(old)
    c['pid_antigo_reutilizado'] = {'create': fmt(po.create_time()), 'scripts': scripts(po)}
np_ = psutil.Process(new)
c['novo'] = {'existe': np_.is_running(), 'status': np_.status(), 'create_time': fmt(np_.create_time()), 'criado_apos_installed_at_s': round(np_.create_time() - installed_at, 2), 'ppid': np_.ppid(), 'scripts': scripts(np_), 'nome': np_.name()}
sp = psutil.Process(sup)
c['supervisor'] = {'existe': sp.is_running(), 'status': sp.status(), 'create_time_exato': repr(sp.create_time()), 'created_gravado_maintenance': repr(mt['supervisor_created']), 'igual_exato': sp.create_time() == mt['supervisor_created'] == rs['supervisor_created'],
                   'create_time_local': fmt(sp.create_time()), 'scripts': scripts(sp), 'flags': flags(sp), 'ppid': sp.ppid()}
c['novo_e_filho_do_mesmo_supervisor'] = (np_.ppid() == sup) and (np_.parent() is not None) and (np_.parent().create_time() == mt['supervisor_created'])
webs = []
for pr in psutil.process_iter(['name']):
    try:
        if (pr.info.get('name') or '').casefold() == 'python.exe' and 'iald_web_server.py' in scripts(pr):
            webs.append(pr.pid)
    except psutil.Error:
        pass
c['processos_iald_web_server'] = webs
ls8082 = [x for x in psutil.net_connections(kind='tcp') if x.status == psutil.CONN_LISTEN and x.laddr.port == 8082]
c['ouvintes_8082'] = [{'ip': x.laddr.ip, 'pid': x.pid} for x in ls8082]
c['ouvinte_8082_e_o_pid_novo'] = bool(ls8082) and all(x.pid == new for x in ls8082)
conn = http.client.HTTPConnection('127.0.0.1', 8082, timeout=15)
try:
    conn.request('GET', '/login')
    resp = conn.getresponse()
    body = resp.read(2_000_000)
    c['GET_login'] = {'status': resp.status, 'bytes': len(body), 'content_type': resp.getheader('Content-Type')}
except Exception as e:
    c['GET_login'] = {'status': 'ERRO:' + repr(e)}
finally:
    conn.close()
# bancada (18765/18766) e modelo local (8081): iguais aos listeners_before/after do deployment
lb, la = sm['listeners_before'], sm['listeners_after']
srv = {}
for port in ('18765', '18766', '8081'):
    ls = [x for x in psutil.net_connections(kind='tcp') if x.status == psutil.CONN_LISTEN and x.laddr.port == int(port)]
    now_rows = []
    for pid in sorted({x.pid for x in ls if x.pid}):
        pr = psutil.Process(pid)
        now_rows.append({'pid': pid, 'create_time': pr.create_time(), 'nome': pr.name(), 'scripts': scripts(pr)})
    simplified = [{'pid': r['pid'], 'create_time': r['create_time']} for r in now_rows]
    srv[port] = {'de_pe_agora': bool(now_rows), 'agora': now_rows, 'before_do_deployment': lb.get(port), 'after_do_deployment': la.get(port), 'igual_before_e_after': lb.get(port) == la.get(port), 'agora_igual_ao_after': simplified == la.get(port)}
c['servicos_nao_reiniciados'] = srv
# log do supervisor: a sequencia do reinicio conta o mesmo pid
sup_log = (R / 'logs' / 'web-supervisor.log').read_text('utf-8', errors='replace').splitlines()
tail = [l for l in sup_log[-40:] if '2026-11-04 14:5' in l]
c['log_do_supervisor_14h5x'] = tail
c['log_diz_PID_novo'] = any(('PID %d iniciado' % new) in l for l in tail)
c['novo_create_time_bate_com_o_log_14:52:10'] = abs(np_.create_time() - datetime(2026, 11, 4, 14, 52, 10).timestamp()) < 3.0
ok = (rs['status'] == 'PASS' and rs['http_status'] == 200 and c['maintenance_json_identidade_igual_restart_json'] and not c['pid_antigo_existe'] and c['novo']['existe'] and c['novo']['status'] != psutil.STATUS_STOPPED
      and c['novo_e_filho_do_mesmo_supervisor'] and c['supervisor']['igual_exato'] and c['supervisor']['status'] != psutil.STATUS_STOPPED and '-nosupervise' not in [f.casefold() for f in c['supervisor']['flags']]
      and c['ouvinte_8082_e_o_pid_novo'] and c['GET_login'].get('status') == 200 and webs == [new] and c['novo']['criado_apos_installed_at_s'] > 0
      and all(v['igual_before_e_after'] and v['agora_igual_ao_after'] for v in srv.values()) and c['log_diz_PID_novo'] and c['novo_create_time_bate_com_o_log_14:52:10'])
res = {'PASS': bool(ok), 'checks': c, 'guard_events': {k: (v if not isinstance(v, list) else v) for k, v in L.EVENTS.items()}}
(HERE / 'r2_d5_out.json').write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
print('D5', 'PASS' if ok else 'FAIL')
print(json.dumps(res, ensure_ascii=False, indent=1)[:6500])
