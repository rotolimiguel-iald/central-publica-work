# -*- coding: utf-8 -*-
"""Teste do escopo MEDIDO do transaction.py (somente leitura no sistema vivo; nada e' escrito fora deste arquivo de evidencia).
Casos: (1) dois snapshots seguidos no sistema vivo -> mede tempo e estabilidade; (2) mutacao SINTETICA num estado de brinquedo (pasta temporaria) -> accounts_modified/client_files_changed
viram True e o mesmo estado sem mutacao vira False; (3) falha de leitura simulada -> None (nao medido), nunca False; (4) mudanca de listener -> bench_restarted True."""
import copy
import json
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
W = Path(__file__).resolve().parent
sys.path.insert(0, str(W))
import transaction as T  # noqa: E402

out = {"casos": {}}

# (1) sistema vivo
a = T.scope_snapshot([])
b = T.scope_snapshot([])
c = T.scope_compare(a, b)
out["casos"]["vivo_dois_snapshots"] = {
    "state_files": len(a["state"]), "client_files": len(a["client"]), "seconds": [a["seconds"], b["seconds"]], "errors": c["scope_measurement"]["errors"],
    "accounts_modified": c["accounts_modified"], "bench_restarted": c["bench_restarted"], "client_files_changed": c["client_files_changed"],
    "state_changed_entre_os_dois": c["scope_measurement"]["state_changed"], "client_changed": c["scope_measurement"]["client_changed"],
    "bench_running": c["scope_measurement"]["bench_running_before"], "local_model_listeners_before": a["listeners"].get("8081"),
}

# (2) mutacao sintetica: monta um "ROOT" de brinquedo e aponta o modulo para ele
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / ".iald_runtime" / "monthly_wallet").mkdir(parents=True)
    (root / ".iald_runtime" / "monthly_wallet" / "wallet.sqlite3").write_bytes(b"carteira-v1")
    (root / "iald_users.json").write_bytes(b'{"u":1}')
    (root / "iald-app" / "www").mkdir(parents=True)
    (root / "iald-app" / "www" / "app.js").write_bytes(b"console.log(1)")
    (root / "iald_web" / "app").mkdir(parents=True)
    (root / "iald_web" / "app" / "index.html").write_bytes(b"<html>")
    old_root = T.ROOT
    T.ROOT = root
    try:
        before = T.scope_snapshot([])
        same = T.scope_snapshot([])
        c_same = T.scope_compare(before, same)
        (root / "iald_users.json").write_bytes(b'{"u":2}')                                  # conta mudou
        (root / "iald-app" / "www" / "app.js").write_bytes(b"console.log(2)")               # cliente mudou
        after = T.scope_snapshot([])
        c_mut = T.scope_compare(before, after)
        # (3) falha de leitura simulada, SEM mudanca observada: um grupo com erro => None (nao medido), nunca False. (Com mudanca observada o certo e' True: ver 'sintetico_com_mutacao'.)
        broken = copy.deepcopy(same)
        broken["errors"].append({"group": "state", "error": "SIMULADO"})
        c_err = T.scope_compare(before, broken)
        # (3b) arquivo ilegivel simulado, sem mudanca observada nos demais
        unread = copy.deepcopy(same)
        k = next(iter(unread["client"]))
        unread["client"][k] = {"error": "PermissionError: simulado"}
        c_unread = T.scope_compare(before, unread)
        # (3c) arquivo travado (*.lock) nao entra na medicao
        (root / ".iald_runtime" / "monthly_wallet" / "web-runtime.lock").write_bytes(b"pid")
        with_lock = T.scope_snapshot([])
        lock_excluded = not any(x.endswith("web-runtime.lock") for x in with_lock["state"])
        # (4) listener: bench passou a ter outro pid
        moved = copy.deepcopy(same)
        moved["listeners"]["18765"] = [{"pid": 999999, "create_time": 1.0}]
        c_bench = T.scope_compare(before, moved)
    finally:
        T.ROOT = old_root
    out["casos"]["sintetico_sem_mutacao"] = {k: c_same[k] for k in ("accounts_modified", "bench_restarted", "client_files_changed")}
    out["casos"]["sintetico_com_mutacao"] = {k: c_mut[k] for k in ("accounts_modified", "bench_restarted", "client_files_changed")}
    out["casos"]["sintetico_com_mutacao"]["state_changed"] = [Path(x).name for x in c_mut["scope_measurement"]["state_changed"]]
    out["casos"]["sintetico_com_mutacao"]["client_changed"] = [Path(x).name for x in c_mut["scope_measurement"]["client_changed"]]
    out["casos"]["falha_de_leitura_do_grupo_state"] = {k: c_err[k] for k in ("accounts_modified", "bench_restarted", "client_files_changed")}
    out["casos"]["arquivo_ilegivel_no_cliente"] = {k: c_unread[k] for k in ("accounts_modified", "bench_restarted", "client_files_changed")}
    out["casos"]["listener_do_bench_mudou"] = {k: c_bench[k] for k in ("accounts_modified", "bench_restarted", "client_files_changed")}
    out["casos"]["trava_lock_excluida"] = {"excluida": lock_excluded}

ok = (
    out["casos"]["sintetico_sem_mutacao"] == {"accounts_modified": False, "bench_restarted": False, "client_files_changed": False}
    and out["casos"]["sintetico_com_mutacao"]["accounts_modified"] is True and out["casos"]["sintetico_com_mutacao"]["client_files_changed"] is True
    and out["casos"]["falha_de_leitura_do_grupo_state"]["accounts_modified"] is None
    and out["casos"]["arquivo_ilegivel_no_cliente"]["client_files_changed"] is None
    and out["casos"]["listener_do_bench_mudou"]["bench_restarted"] is True
    and out["casos"]["trava_lock_excluida"]["excluida"] is True
    and not out["casos"]["vivo_dois_snapshots"]["errors"]
    and out["casos"]["vivo_dois_snapshots"]["accounts_modified"] is False   # no vivo, com o web de pe e sem trava, dois snapshots seguidos nao diferem
)
out["passou"] = ok
raw = json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8")
with (W / "TESTE_ESCOPO_v407.json").open("xb") as f:
    f.write(raw)
print(raw.decode("utf-8"))
sys.exit(0 if ok else 1)
