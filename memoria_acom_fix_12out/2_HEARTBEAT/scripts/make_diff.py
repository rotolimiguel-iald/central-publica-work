# -*- coding: utf-8 -*-
"""Gera DIFF.patch: diff unificado entre originais\\ (bytes de producao, sha256 em evidencias\\ORIGINAIS_12out.json)
e copia\\projetos_pyhton\\IALD\\ (os arquivos modificados). Usa difflib (stdlib) sobre o texto decodificado em UTF-8
com os fins de linha preservados (CRLF), para que o patch aplique byte a byte com `git apply` / `patch`.
Grava tambem evidencias\\DIFF_STATS.json (linhas +/-, sha256 antes/depois, CRLF conferido).
"""
import difflib, hashlib, json, os
from datetime import datetime

FRONT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIG = os.path.join(FRONT, "originais")
COPIA = os.path.join(FRONT, "copia", "projetos_pyhton", "IALD")
PROD = r"C:\IALD\projetos_pyhton\IALD"
FILES = ["iald_web_server.py", "iald_app_memory.py"]


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    chunks, stats = [], {"at": datetime.now().isoformat(timespec="seconds"), "files": []}
    for name in FILES:
        a_raw = open(os.path.join(ORIG, name), "rb").read()
        b_raw = open(os.path.join(COPIA, name), "rb").read()
        prod_raw = open(os.path.join(PROD, name), "rb").read()
        a = a_raw.decode("utf-8").splitlines(keepends=True)
        b = b_raw.decode("utf-8").splitlines(keepends=True)
        rel = "projetos_pyhton/IALD/" + name
        diff = list(difflib.unified_diff(a, b, fromfile="a/" + rel, tofile="b/" + rel, n=3))
        chunks.append("diff --git a/%s b/%s\n" % (rel, rel))
        chunks.append("index %s..%s 100644\n" % (sha256(a_raw)[:12], sha256(b_raw)[:12]))
        chunks.extend(diff)
        added = sum(1 for l in diff if l.startswith("+") and not l.startswith("+++"))
        removed = sum(1 for l in diff if l.startswith("-") and not l.startswith("---"))
        stats["files"].append({"file": rel, "sha256_original": sha256(a_raw), "sha256_production_now": sha256(prod_raw),
                               "production_equals_original": prod_raw == a_raw, "sha256_modified": sha256(b_raw),
                               "bytes_original": len(a_raw), "bytes_modified": len(b_raw), "lines_added": added, "lines_removed": removed,
                               "crlf_only_original": a_raw.count(b"\r\n") == a_raw.count(b"\n"),
                               "crlf_only_modified": b_raw.count(b"\r\n") == b_raw.count(b"\n")})
    patch = "".join(chunks)
    out = os.path.join(FRONT, "DIFF.patch")
    with open(out, "wb") as f:
        f.write(patch.encode("utf-8"))
    stats["patch"] = {"path": out, "bytes": len(patch.encode("utf-8")), "sha256": sha256(patch.encode("utf-8"))}
    with open(os.path.join(FRONT, "evidencias", "DIFF_STATS.json"), "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=1)
    print(json.dumps(stats, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
