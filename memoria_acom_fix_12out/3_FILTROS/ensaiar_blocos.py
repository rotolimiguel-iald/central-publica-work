"""Ensaio do D5 em cópias: copia `blocos\\copias\\*` para `blocos\\ensaio\\` e aplica o
`aplicar_blocos.py` (cinco superfícies + MEMORY.md + SESSION_BRIDGE.md), gerando
`blocos\\BLOCOS_RECIBO.json`. Os originais de produção e as cópias de referência ficam intactos.
"""
from __future__ import annotations
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COPIAS = ROOT / "blocos" / "copias"
ENSAIO = ROOT / "blocos" / "ensaio"
FIVE = ["CLAUDE_global.md", "AGENTS.md", "CLAUDE_nativa.md", "README.md", "COORDINATOR.md"]


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    if ENSAIO.exists():
        shutil.rmtree(ENSAIO)
    ENSAIO.mkdir(parents=True)
    for name in FIVE + ["MEMORY.md"]:
        shutil.copyfile(COPIAS / name, ENSAIO / name)
    shutil.copyfile(ROOT / "originais" / "C" / "IALD" / "MEMORIA_IALD" / "SESSION_BRIDGE.md", ENSAIO / "SESSION_BRIDGE.md")
    before = {name: sha256(ENSAIO / name) for name in FIVE + ["MEMORY.md", "SESSION_BRIDGE.md"]}
    argv = [sys.executable, "-X", "utf8", "-B", str(ROOT / "aplicar_blocos.py"), "--recibo", str(ROOT / "blocos" / "BLOCOS_RECIBO.json"),
            "--memory-md", str(ENSAIO / "MEMORY.md")]
    for name in FIVE + ["SESSION_BRIDGE.md"]:
        argv += ["--alvo", str(ENSAIO / name)]
    proc = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8")
    print(proc.stdout.strip()); print(proc.stderr.strip())
    after = {name: sha256(ENSAIO / name) for name in before}
    untouched = {name: sha256(COPIAS / name) for name in FIVE + ["MEMORY.md"]}
    origem = json.loads((ROOT / "ORIGINAIS.json").read_text(encoding="utf-8"))
    ref = {Path(s["copia"]).name: s["sha256"] for s in origem["superficies"]}
    assert all(untouched[n] == ref[n] for n in untouched), "cópias de referência mudaram"
    summary = {"returncode": proc.returncode, "before": before, "after": after, "copias_intactas": True,
               "backups": sorted(p.name for p in ENSAIO.glob("*.bak_*"))}
    (ROOT / "blocos" / "ENSAIO_RESUMO.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"returncode": proc.returncode, "changed": [n for n in before if before[n] != after[n]], "backups": len(summary["backups"])}))
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
