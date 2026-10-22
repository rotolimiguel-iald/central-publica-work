"""Gera DIFF.patch (unified diff) entre `originais\\` e `copia\\` para cada arquivo da frente;
`guard.py` entra como arquivo novo. Caminhos no cabeçalho são os de PRODUÇÃO (a/… = original
instalado; b/… = cópia modificada), para a instalação M3 aplicar sem adivinhação.
Linhas lidas como BYTES (surrogateescape, sem tradução de fim de linha): arquivo CRLF gera patch
CRLF e `git apply` reproduz `copia\\` byte a byte. Corrigido em 13/10/2026: a versão anterior usava
read_text e perdia os \\r do iald_app_memory.py (555 CRLF no original). Conferência: aplicar num
repositório git descartável (fora do repo da Central, que faria o `git apply` ignorar os caminhos)."""
from __future__ import annotations
import difflib
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ORIG = ROOT / "originais" / "C"
COPIA = ROOT / "copia" / "C"
FILES = [
    "IALD/MEMORIA_IALD/session_memory.py",
    "IALD/MEMORIA_IALD/SESSION_BRIDGE.md",
    "IALD/MEMORIA_IALD/lib/iald_memory/__init__.py",
    "IALD/MEMORIA_IALD/lib/iald_memory/guard.py",
    "IALD/projetos_pyhton/IALD/iald_app_memory.py",
    "IALD/Central de Patentes/Chatgpt/IALD_ORQUESTRACAO_20260923/iald_orchestrator/policy.py",
    "IALD/Central de Patentes/Chatgpt/IALD_ORQUESTRACAO_20260923/iald_orchestrator/operational_memory.py",
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None


def lines(path):
    """Bytes -> text lines keeping their exact terminators (CRLF preserved); never lossy."""
    return [chunk.decode("utf-8", "surrogateescape") for chunk in path.read_bytes().splitlines(keepends=True)]


def main():
    out, summary = [], []
    for rel in FILES:
        a, b = ORIG / rel, COPIA / rel
        prod = "C/" + rel  # árvore espelhada: C/ = C:\ (a/ = originais\C, b/ = copia\C); `git apply --check` valida contra originais\
        old = lines(a) if a.exists() else []
        new = lines(b)
        diff = list(difflib.unified_diff(old, new, fromfile=("a/" + prod) if a.exists() else "/dev/null", tofile="b/" + prod, n=3))
        # A last line without terminator (e.g. the original __init__.py) needs git's marker, or `git apply` refuses.
        diff = [l if l.endswith("\n") or i < 2 else l + "\n\\ No newline at end of file\n" for i, l in enumerate(diff)]
        header = "diff --git a/%s b/%s\n" % (prod, prod)
        if not a.exists():
            header += "new file mode 100644\n"
        header += "index %s..%s\n" % ((sha(a) or "0" * 64)[:16], sha(b)[:16])
        out.append(header + "".join(diff) + ("\n" if diff and not diff[-1].endswith("\n") else ""))
        added = sum(1 for l in diff if l.startswith("+") and not l.startswith("+++"))
        removed = sum(1 for l in diff if l.startswith("-") and not l.startswith("---"))
        summary.append({"file": prod, "new_file": not a.exists(), "old_sha256": sha(a), "new_sha256": sha(b),
                        "lines_added": added, "lines_removed": removed, "old_bytes": a.stat().st_size if a.exists() else 0,
                        "new_bytes": b.stat().st_size})
    (ROOT / "DIFF.patch").write_bytes("".join(out).encode("utf-8", "surrogateescape"))
    (ROOT / "DIFF_RESUMO.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"files": len(summary), "added": sum(s["lines_added"] for s in summary),
                      "removed": sum(s["lines_removed"] for s in summary), "patch_bytes": (ROOT / "DIFF.patch").stat().st_size}))


if __name__ == "__main__":
    main()
