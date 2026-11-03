# -*- coding: utf-8 -*-
"""Guarda a rodada r1 em superseded_r1/ (movida, nunca apagada) e invalida na missao as tarefas sources e app, depois do parecer de recusa."""
import hashlib
import json
import shutil
from pathlib import Path

import task

W = task.W
S = W / "superseded_r1"
ITENS = ["app/BUILT.json", "app/DATA_PLAN.json", "app/DELIVERY_PREPARED.json", "app/NATIVE_COUNTS_COMPLETE.json", "app/PREPARED_BINDING.json",
         "app/PUBLIC_GIT_BINDING.json", "app/RUNTIME_BASELINE.json", "app/packages", "app/science", "install_plan.json", "sources_verified.json",
         "BUILDER_MEASUREMENTS.json", "BUSCA_EXERCITADA_v405.txt", "validation/final_checks.json", "validation/review_findings.json",
         "validation/review_app_independent.json", "validation/review_sources.json"]
ITENS += [p.name for p in W.glob("*_stdout.txt")] + [p.name for p in W.glob("*_stderr.txt")]
ITENS += [p.relative_to(W).as_posix() for p in (W / "app").glob("native_prefix*")]
assert not S.exists()
movidos = []
for rel in ITENS:
    origem = W / rel
    assert origem.exists(), rel
    destino = S / rel
    destino.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(origem), str(destino))
    movidos.append(rel)
(S / "MOVED_MANIFEST.json").write_text(json.dumps({
    "reason": "r1 recusada pelo revisor independente (achado F1 bloqueante; F2, F3, F4 baixos); movida, nao apagada; a evidencia r1 fica pinada no historico da missao (recibos v405-*-submit.json)",
    "moved_items": movidos}, ensure_ascii=False, indent=1), encoding="utf-8")


def pin(p):
    p = Path(p)
    return {"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}


parecer = S / "validation" / "review_findings.json"
for tarefa in ("sources", "app"):
    p = task.project()
    r = task.call({"operation": "invalidate", "reference": str(task.REF), "actor": {"id": task.OWNER, "kind": "agent"},
                   "expected_revision": p["receipt"]["revision"], "projection_sha256": p["projection_sha256"],
                   "state_sha256": p["receipt"]["state_sha256"], "task_id": tarefa, "sources": [pin(parecer)],
                   "reason": "Parecer r1 do revisor independente recusou: a frase da capsula valia so pelo nome (F1). Reconstrucao r2 com a regra por familia.",
                   "event_id": "v405-%s-invalidate-r2" % tarefa})
    (W / "receipts" / ("v405-%s-invalidate-r2.json" % tarefa)).write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    print(tarefa, r["receipt"]["revision"], (r.get("task") or {}).get("status"))
print(json.dumps({"movidos": len(movidos)}, ensure_ascii=False))
