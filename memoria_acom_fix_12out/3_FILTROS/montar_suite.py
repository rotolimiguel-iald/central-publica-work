"""Monta `suite\\` (harness das suítes) a partir de `copia\\` (código da frente), de `originais\\`
(código inalterado) e dos arquivos de apoio da origem instalada. As cópias em `suite\\` são
conferidas por sha256 contra `copia\\` — a suíte testa exatamente o que será instalado.
Nada em produção é tocado; os arquivos de apoio são lidos, nunca escritos.
"""
from __future__ import annotations
import hashlib
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COPIA = ROOT / "copia" / "C"
ORIG = ROOT / "originais" / "C"
SUITE = ROOT / "suite"
ORIGEM = Path(r"C:\IALD\Central de Patentes\work\iald_memoria_acom_20261010")
APP_PROD = Path(r"C:\IALD\projetos_pyhton\IALD")
QUEUE_PROD = Path(r"C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\iald_orchestrator")
AUDIT_GUARD = Path(r"C:\IALD\PROGRAMA_IALD\exame_12out\E_ACOM\guard\sitecustomize.py")


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def put(src, dst, manifest, role):
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    data = Path(src).read_bytes()
    tmp = dst.with_name(dst.name + ".tmp_suite")
    tmp.write_bytes(data)
    if tmp.read_bytes() != data:
        raise RuntimeError("cópia divergente: " + str(dst))
    os.replace(tmp, dst)
    manifest.append({"role": role, "source": str(src), "target": str(dst), "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})


def main():
    manifest = []
    # core: __init__ + guard (frente) + store (inalterado, original)
    core = SUITE / "core" / "iald_memory"
    put(COPIA / "IALD/MEMORIA_IALD/lib/iald_memory/__init__.py", core / "__init__.py", manifest, "frente")
    put(COPIA / "IALD/MEMORIA_IALD/lib/iald_memory/guard.py", core / "guard.py", manifest, "frente")
    put(ORIG / "IALD/MEMORIA_IALD/lib/iald_memory/store.py", core / "store.py", manifest, "original")
    # sessions: CLI (frente) + hook (original) + testes da origem
    sessions = SUITE / "sessions"
    put(COPIA / "IALD/MEMORIA_IALD/session_memory.py", sessions / "session_memory.py", manifest, "frente")
    put(ORIG / "IALD/MEMORIA_IALD/session_hook.py", sessions / "session_hook.py", manifest, "original")
    for name in ("test_sessions.py", "test_hooks.py"):
        put(ORIGEM / "sessions" / name, sessions / name, manifest, "teste_origem")
    # app: adaptador (frente) + apoio instalado (lido de produção, byte-igual à origem) + teste da origem
    app = SUITE / "app"
    put(COPIA / "IALD/projetos_pyhton/IALD/iald_app_memory.py", app / "iald_app_memory.py", manifest, "frente")
    for name in ("iald_web_server.py", "iald_app_providers.py", "iald_auto_router.py", "iald_task_bridge.py",
                 "iald_motores.py", "iald_memoria_operador.py", "iald_jev_control.py"):
        put(APP_PROD / name, app / name, manifest, "apoio_instalado")
    put(ORIGEM / "app" / "test_app_memory.py", app / "test_app_memory.py", manifest, "teste_origem")
    # queue: pacote instalado (.py, sem .bak_) com policy/operational_memory da frente
    queue = SUITE / "queue" / "iald_orchestrator"
    for entry in sorted(QUEUE_PROD.iterdir()):
        if entry.suffix == ".py" and ".bak_" not in entry.name:
            put(entry, queue / entry.name, manifest, "apoio_instalado")
    put(COPIA / "IALD/Central de Patentes/Chatgpt/IALD_ORQUESTRACAO_20260923/iald_orchestrator/policy.py", queue / "policy.py", manifest, "frente")
    put(COPIA / "IALD/Central de Patentes/Chatgpt/IALD_ORQUESTRACAO_20260923/iald_orchestrator/operational_memory.py", queue / "operational_memory.py", manifest, "frente")
    # guarda de execução da auditoria (sitecustomize por PYTHONPATH)
    put(AUDIT_GUARD, ROOT / "guard_exec" / "sitecustomize.py", manifest, "guarda_auditoria")
    # conferência: toda cópia "frente" é byte-igual à de copia\
    for item in manifest:
        if item["role"] == "frente":
            assert sha256(item["source"]) == item["sha256"] == sha256(item["target"]), item
    (SUITE / "__init__.py").touch(exist_ok=True)
    out = {"at": datetime.now(timezone.utc).isoformat(), "files": manifest}
    (ROOT / "SUITE_MANIFEST.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"files": len(manifest), "frente": sum(i["role"] == "frente" for i in manifest)}))


if __name__ == "__main__":
    main()
