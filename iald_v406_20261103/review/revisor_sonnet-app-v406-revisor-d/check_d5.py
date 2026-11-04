# -*- coding: utf-8 -*-
"""Revisor independente da INSTALACAO v406 - D5 (processos). Somente leitura; unica rede: GET http://127.0.0.1:8082/login."""
import sys
sys.dont_write_bytecode = True
import json, time, http.client, hashlib
from pathlib import Path
from datetime import datetime
import psutil

W = Path("C:/IALD/Central de Patentes/work/iald_v406_20261103")
OUT = W / "review/revisor_sonnet-app-v406-revisor-d"
rs = json.loads((W / "restart.json").read_bytes())
dep = json.loads((W / "deployment.json").read_bytes())
mt = json.loads((W / "maintenance.json").read_bytes())
installed_at = datetime.fromisoformat(dep["installed_at"]).timestamp()
LIMIAR = time.mktime((2026, 11, 3, 20, 18, 0, 0, 0, -1))  # 03/11/2026 20:18 local


def fmt(ts):
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S.%f")


def scripts(p):
    try:
        return [Path(a).name for a in p.cmdline()[1:] if a and not a.startswith("-")][:3]
    except Exception as e:  # noqa
        return ["ERRO:" + type(e).__name__]


old, new, sup = rs["old_web_pid"], rs["new_web_pid"], rs["supervisor_pid"]
R = {"restart.json": {k: rs[k] for k in ("old_web_pid", "new_web_pid", "supervisor_pid", "supervisor_created", "status", "http_status")},
     "maintenance.json_identidade_igual": {k: mt[k] for k in ("old_web_pid", "supervisor_pid", "supervisor_created")} == {k: rs[k] for k in ("old_web_pid", "supervisor_pid", "supervisor_created")}}
c = {}

# pid antigo
c["pid_antigo_existe"] = psutil.pid_exists(old)
if c["pid_antigo_existe"]:
    p = psutil.Process(old)
    c["pid_antigo_reutilizado"] = {"create": fmt(p.create_time()), "scripts": scripts(p)}

# pid novo
np_ = psutil.Process(new)
c["novo_existe"] = np_.is_running()
c["novo_status"] = np_.status()
c["novo_create_time"] = fmt(np_.create_time())
c["novo_criado_apos_installed_at"] = np_.create_time() > installed_at
c["novo_segundos_apos_installed_at"] = round(np_.create_time() - installed_at, 2)
c["novo_ppid"] = np_.ppid()
c["novo_scripts"] = scripts(np_)
c["novo_nome"] = np_.name()

# supervisor
sp = psutil.Process(sup)
c["supervisor_existe"] = sp.is_running()
c["supervisor_status"] = sp.status()
c["supervisor_create_time_exato"] = repr(sp.create_time())
c["supervisor_created_gravado"] = repr(rs["supervisor_created"])
c["supervisor_create_igual_exato"] = (sp.create_time() == rs["supervisor_created"])
c["supervisor_create_diff_s"] = abs(sp.create_time() - rs["supervisor_created"])
c["supervisor_create_local"] = fmt(sp.create_time())
c["supervisor_scripts"] = scripts(sp)
c["novo_e_filho_do_supervisor"] = (np_.ppid() == sup) and (np_.parent() is not None) and (np_.parent().create_time() == rs["supervisor_created"])

# unico filho web
webs = []
for pr in psutil.process_iter(["name"]):
    try:
        if (pr.info.get("name") or "").casefold() == "python.exe" and "iald_web_server.py" in scripts(pr):
            webs.append(pr.pid)
    except psutil.Error:
        pass
c["processos_iald_web_server"] = webs

# ouvinte 8082
ls = [x for x in psutil.net_connections(kind="tcp") if x.status == psutil.CONN_LISTEN and x.laddr.port == 8082]
c["ouvintes_8082"] = [{"ip": x.laddr.ip, "pid": x.pid} for x in ls]
c["ouvinte_8082_e_pid_novo"] = bool(ls) and all(x.pid == new for x in ls)

# GET /login
conn = http.client.HTTPConnection("127.0.0.1", 8082, timeout=15)
try:
    conn.request("GET", "/login")
    resp = conn.getresponse()
    body = resp.read(2_000_000)
    c["GET_login_status"] = resp.status
    c["GET_login_bytes"] = len(body)
except Exception as e:  # noqa
    c["GET_login_status"] = "ERRO:" + repr(e)
finally:
    conn.close()

# servicos que nao devem ter sido reiniciados
srv = {}
for port in (18765, 18766, 8081):
    l2 = [x for x in psutil.net_connections(kind="tcp") if x.status == psutil.CONN_LISTEN and x.laddr.port == port]
    if not l2:
        srv[str(port)] = {"de_pe": False}
        continue
    pids = sorted({x.pid for x in l2 if x.pid})
    rows = []
    for pid in pids:
        pr = psutil.Process(pid)
        rows.append({"pid": pid, "nome": pr.name(), "create": fmt(pr.create_time()), "scripts": scripts(pr),
                     "antes_de_20h18": pr.create_time() < LIMIAR})
    srv[str(port)] = {"de_pe": True, "procs": rows, "todos_antes_de_20h18": all(r["antes_de_20h18"] for r in rows)}
c["servicos_nao_reiniciados"] = srv
c["installed_at_local"] = fmt(installed_at)
c["limiar_local"] = fmt(LIMIAR)

ok = (rs["status"] == "PASS" and rs["http_status"] == 200 and not c["pid_antigo_existe"] and c["novo_existe"]
      and c["novo_status"] != psutil.STATUS_STOPPED and c["novo_e_filho_do_supervisor"] and c["supervisor_create_igual_exato"]
      and c["supervisor_status"] != psutil.STATUS_STOPPED and c["ouvinte_8082_e_pid_novo"] and c["GET_login_status"] == 200
      and webs == [new] and c["novo_criado_apos_installed_at"] and R["maintenance.json_identidade_igual"]
      and all((v.get("todos_antes_de_20h18", True)) for v in srv.values()))
R["checks"] = c
R["PASS"] = bool(ok)
(OUT / "d5_result.json").write_text(json.dumps(R, ensure_ascii=False, indent=1), encoding="utf-8")
print("D5", "PASS" if ok else "FAIL")
print(json.dumps(R, ensure_ascii=False, indent=1)[:5500])
