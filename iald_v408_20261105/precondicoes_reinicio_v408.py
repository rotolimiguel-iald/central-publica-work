# -*- coding: utf-8 -*-
"""Pre-condicoes do reinicio do filho web (porta 8082), SOMENTE LEITURA: nao suspende, nao mata, nao inicia nada, nao escreve na producao.
(1) quiet() da v408 (trabalho ativo recusa); (2) scope_snapshot + scope_compare VIVOS (B2 do parecer: pega excecao antes de a instalacao depender deles);
(3) a topologia que maintenance.stopped_web exige: exatamente 1 filho web, pai = start_iald_web.ps1 sem -NoSupervise, 1 listener na 8082 que e' o filho;
(4) o baseline do plano ainda bate com a producao (nenhum destino mudou desde o plano). Grava um recibo (xb) por execucao com carimbo no nome."""
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path

sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
sys.path.insert(0, str(W))
import transaction as T  # noqa: E402
import maintenance as M  # noqa: E402

out = {"quando": datetime.now().astimezone().isoformat(timespec="seconds"), "somente_leitura": True}

# (1) quiet()
try:
    out["quiet"] = {"ok": True, **T.quiet()}
except Exception as exc:
    out["quiet"] = {"ok": False, "recusou": type(exc).__name__ + ": " + str(exc)[:200]}

# (2) escopo medido vivo (dois snapshots seguidos; sem plano de destinos)
plan = json.loads((W / "install_plan.json").read_bytes())
dests = [i["destination"] for i in plan["files"]]
try:
    a = T.scope_snapshot(dests)
    b = T.scope_snapshot(dests)
    c = T.scope_compare(a, b)
    sm = c["scope_measurement"]
    out["escopo_vivo"] = {"ok": True, "accounts_modified": c["accounts_modified"], "bench_restarted": c["bench_restarted"], "client_files_changed": c["client_files_changed"],
                          "state_files": sm["state_files"], "client_files": sm["client_files"], "errors": sm["errors"], "state_changed_entre_dois_snapshots": sm["state_changed"],
                          "plan_overlap": a["plan_overlap"], "seconds": [a["seconds"], b["seconds"]]}
except Exception as exc:
    out["escopo_vivo"] = {"ok": False, "excecao": type(exc).__name__ + ": " + str(exc)[:200]}

# (3) topologia do web (leitura de processos; nada e' suspenso)
try:
    web = M._web_processes()
    listeners = M._listeners()
    topo = {"filhos_web": [p.pid for p in web], "listeners_8082": [(c.pid) for c in listeners]}
    if len(web) == 1:
        child = web[0]
        parent = child.parent()
        topo["pai_pid"] = parent.pid if parent else None
        topo["pai_e_start_iald_web_ps1"] = bool(parent) and M._has_script(parent, M.ROOT / "start_iald_web.ps1")
        topo["pai_sem_nosupervise"] = bool(parent) and not any(a.casefold() == "-nosupervise" for a in parent.cmdline())
        topo["listener_e_o_filho"] = len(listeners) == 1 and listeners[0].pid == child.pid
        topo["pai_create_time"] = parent.create_time() if parent else None
        topo["filho_create_time"] = child.create_time()
    topo["ok"] = bool(len(web) == 1 and topo.get("pai_e_start_iald_web_ps1") and topo.get("pai_sem_nosupervise") and topo.get("listener_e_o_filho"))
    out["topologia_web"] = topo
except Exception as exc:
    out["topologia_web"] = {"ok": False, "excecao": type(exc).__name__ + ": " + str(exc)[:200]}

# (4) baseline do plano x producao agora
mudou = []
for item in plan["files"]:
    dest = Path(item["destination"])
    atual = hashlib.sha256(dest.read_bytes()).hexdigest() if dest.exists() else None
    if atual != item["baseline"]:
        mudou.append(str(dest))
out["baseline_do_plano"] = {"ok": not mudou, "arquivos_no_plano": len(plan["files"]), "destinos_diferentes_do_baseline": mudou[:10]}

out["tudo_ok"] = bool(out["quiet"].get("ok") and out["escopo_vivo"].get("ok") and not out["escopo_vivo"].get("errors") and not out["escopo_vivo"].get("plan_overlap") and out["escopo_vivo"].get("client_files_changed") is False and out["topologia_web"].get("ok") and out["baseline_do_plano"]["ok"])
nome = "PRECONDICOES_REINICIO_v408_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".json"
raw = json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8")
with (W / nome).open("xb") as f:
    f.write(raw)
print(raw.decode("utf-8"))
print("RECIBO:", nome, hashlib.sha256(raw).hexdigest()[:16])
sys.exit(0 if out["tudo_ok"] else 1)
