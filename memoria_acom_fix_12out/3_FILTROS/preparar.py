"""Frente FILTROS (conserto ACOM 12/10): prepara a pasta de trabalho.

Copia BYTES dos originais de produção para `originais\\` (referência do diff) e
para `copia\\` (árvore que espelha a produção, onde os filtros são aplicados), e
copia os cinco arquivos de instrução + MEMORY.md para `blocos\\copias\\`.
Nada em produção é tocado. Todo hash é lido do arquivo por este script.
"""
from __future__ import annotations
import hashlib
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ORIGINAIS = ROOT / "originais"
COPIA = ROOT / "copia"
BLOCOS = ROOT / "blocos" / "copias"

# Arquivos da frente (D4): os que serão modificados e os vizinhos de que as suítes precisam.
FONTES = [
    r"C:\IALD\MEMORIA_IALD\session_memory.py",
    r"C:\IALD\MEMORIA_IALD\session_hook.py",
    r"C:\IALD\MEMORIA_IALD\SESSION_BRIDGE.md",
    r"C:\IALD\MEMORIA_IALD\lib\iald_memory\__init__.py",
    r"C:\IALD\MEMORIA_IALD\lib\iald_memory\store.py",
    r"C:\IALD\projetos_pyhton\IALD\iald_app_memory.py",
    r"C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\iald_orchestrator\policy.py",
    r"C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\iald_orchestrator\operational_memory.py",
    r"C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\iald_orchestrator\nos_packet.py",
]
# Os que a frente MODIFICA (os demais ficam em `copia\` só se forem byte-iguais ao original).
MODIFICADOS = {
    r"C:\IALD\MEMORIA_IALD\session_memory.py",
    r"C:\IALD\MEMORIA_IALD\SESSION_BRIDGE.md",
    r"C:\IALD\MEMORIA_IALD\lib\iald_memory\__init__.py",
    r"C:\IALD\projetos_pyhton\IALD\iald_app_memory.py",
    r"C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\iald_orchestrator\policy.py",
    r"C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\iald_orchestrator\operational_memory.py",
}
# Superfícies D5 (cópias para o ensaio do aplicar_blocos.py).
SUPERFICIES = [
    r"C:\Users\rotol\.claude\CLAUDE.md",
    r"C:\Users\rotol\.codex\AGENTS.md",
    r"C:\IALD\projetos_pyhton\IALD\CLAUDE.md",
    r"C:\IALD\PROGRAMA_IALD\README.md",
    r"C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\COORDINATOR.md",
    r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\MEMORY.md",
]
ORDEM = r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_ordem_memoria_remote_rank_qg_bancada_verbatim.txt"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def espelho(base, source):
    """`C:\\x\\y` -> `<base>\\C\\x\\y`."""
    p = Path(source)
    return base / p.drive.rstrip(":") / Path(*p.parts[1:])


def copiar_bytes(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    data = Path(src).read_bytes()
    tmp = dst.with_name(dst.name + ".tmp_prep")
    tmp.write_bytes(data)
    if tmp.read_bytes() != data:
        raise RuntimeError("cópia divergente: " + str(dst))
    os.replace(tmp, dst)
    return len(data)


def main():
    at = datetime.now(timezone.utc).isoformat()
    inventario = {"at": at, "root": str(ROOT), "originais": [], "superficies": [], "ordem": None}
    for src in FONTES:
        st = os.stat(src)
        digest = sha256(src)
        dst_o = espelho(ORIGINAIS, src)
        copiar_bytes(src, dst_o)
        entry = {"source": src, "bytes": st.st_size, "sha256": digest,
                 "mtime": datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds"),
                 "copia_original": str(dst_o), "modificado_pela_frente": src in MODIFICADOS}
        if src in MODIFICADOS:
            dst_c = espelho(COPIA, src)
            copiar_bytes(src, dst_c)
            entry["copia_trabalho"] = str(dst_c)
        if sha256(dst_o) != digest:
            raise RuntimeError("hash divergente após cópia: " + src)
        inventario["originais"].append(entry)
    for src in SUPERFICIES:
        st = os.stat(src)
        dst = BLOCOS / Path(src).name if Path(src).name != "CLAUDE.md" else BLOCOS / (
            "CLAUDE_global.md" if "rotol" in src else "CLAUDE_nativa.md")
        copiar_bytes(src, dst)
        inventario["superficies"].append({"source": src, "bytes": st.st_size, "sha256": sha256(src),
                                          "copia": str(dst), "copia_sha256": sha256(dst)})
    inventario["ordem"] = {"source": ORDEM, "bytes": os.stat(ORDEM).st_size, "sha256": sha256(ORDEM),
                           "linha_1": Path(ORDEM).read_text(encoding="utf-8").splitlines()[0]}
    out = ROOT / "ORIGINAIS.json"
    out.write_text(json.dumps(inventario, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"originais": len(inventario["originais"]), "superficies": len(inventario["superficies"]),
                      "ordem_sha16": inventario["ordem"]["sha256"][:16], "out": str(out)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
