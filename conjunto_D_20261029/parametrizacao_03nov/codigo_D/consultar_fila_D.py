# -*- coding: utf-8 -*-
"""consultar_fila_D.py -- progresso da fila do conjunto D, SEM abrir posterior: le fila/ESTADO_FILA_D.json, F4_1_CONVERGENCIA.json e, por job, so os resumos de convergencia
(CONTROLLER/ANALYST_STATUS/PRIVATE_CONVERGENCE). Roda no Windows ou no WSL.   python consultar_fila_D.py [--json]"""
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

CODE = Path(__file__).resolve().parent
BASE = CODE.parent
sys.path.insert(0, str(CODE))
import lancar_fila_D as L  # noqa: E402


def decorrido_h(ini):
    return (datetime.now(timezone.utc) - datetime.fromisoformat(ini)).total_seconds() / 3600


def resumo():
    est = L.carregar_estado()
    out = {"fase": est.get("fase"), "atualizado_utc": est.get("atualizado_utc"), "pinos_sha256": est.get("pinos_sha256"), "jobs": {}}
    f41 = BASE / "F4_1_CONVERGENCIA.json"
    if f41.exists():
        r = json.loads(f41.read_text(encoding="utf-8"))
        out["F4_1"] = {k: r.get(k) for k in ("convergiu", "status_pe", "delta_logz", "ess", "ncall", "wall_h", "cpu_h", "chamadas_por_s")}
    for n, j in sorted(est.get("jobs", {}).items()):
        d = {"estado": j.get("estado"), "inicio_utc": j.get("inicio_utc"), "fim_utc": j.get("fim_utc")}
        if j.get("estado") == "EM_CURSO" and j.get("inicio_utc"):
            d["decorrido_h"] = round(decorrido_h(j["inicio_utc"]), 2)
        for k in ("status_controlador", "status_pe", "aceito", "ncall", "delta_logz", "ess", "wall_s", "repetir_D5"):
            if j.get(k) is not None:
                d[k] = j[k]
        out["jobs"][n] = d
    cont = {}
    for j in out["jobs"].values():
        cont[j["estado"]] = cont.get(j["estado"], 0) + 1
    out["contagem_por_estado"] = cont
    if est.get("estagio_cego"):
        out["estagio_cego"] = est["estagio_cego"]
    return out


if __name__ == "__main__":
    r = resumo()
    if "--json" in sys.argv:
        print(json.dumps(r, indent=1, ensure_ascii=False))
    else:
        print("fase:", r["fase"], "| atualizado:", r["atualizado_utc"])
        if "F4_1" in r:
            print("F4.1:", r["F4_1"])
        print("jobs por estado:", r["contagem_por_estado"])
        for n, d in r["jobs"].items():
            print(" ", n, {k: v for k, v in d.items() if v is not None})
        if "estagio_cego" in r:
            print("estagio cego:", r["estagio_cego"])
