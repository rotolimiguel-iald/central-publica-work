# -*- coding: utf-8 -*-
"""Gera MANIFESTO.json: sha256 (por script) de todo arquivo da frente HEARTBEAT, mais os sha256 dos originais de
producao lidos agora, da lib v1 congelada e da guarda da auditoria. Exclui tmp\\, guard_log\\ e __pycache__.
O proprio MANIFESTO.json nao se auto-inclui (o seu sha256 e medido pelo leitor).
"""
import hashlib, json, os
from datetime import datetime

FRONT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {"tmp", "guard_log", "__pycache__"}
PROD = {
    "producao/iald_web_server.py": r"C:\IALD\projetos_pyhton\IALD\iald_web_server.py",
    "producao/iald_app_memory.py": r"C:\IALD\projetos_pyhton\IALD\iald_app_memory.py",
    "producao/MEMORIA_IALD/lib/iald_memory/store.py": r"C:\IALD\MEMORIA_IALD\lib\iald_memory\store.py",
    "producao/MEMORIA_IALD/lib/iald_memory/__init__.py": r"C:\IALD\MEMORIA_IALD\lib\iald_memory\__init__.py",
    "auditoria/guard/sitecustomize.py": r"C:\IALD\PROGRAMA_IALD\exame_12out\E_ACOM\guard\sitecustomize.py",
    "ordem_do_operador": r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_ordem_memoria_remote_rank_qg_bancada_verbatim.txt",
    "especificacao/ESPECIFICACAO.md": r"C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\0_DIAGNOSTICO\ESPECIFICACAO.md",
}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    files = []
    for base, dirs, names in os.walk(FRONT):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for name in sorted(names):
            if name == "MANIFESTO.json":
                continue
            p = os.path.join(base, name)
            rel = os.path.relpath(p, FRONT).replace("\\", "/")
            st = os.stat(p)
            files.append({"path": rel, "bytes": st.st_size, "mtime": datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds"),
                          "sha256": sha256(p)})
    externals = {k: ({"path": v, "bytes": os.stat(v).st_size, "sha256": sha256(v)} if os.path.isfile(v) else {"path": v, "missing": True})
                 for k, v in PROD.items()}
    results = json.load(open(os.path.join(FRONT, "tests", "RESULTADOS.json"), encoding="utf-8")) if os.path.isfile(os.path.join(FRONT, "tests", "RESULTADOS.json")) else None
    manifest = {
        "frente": "HEARTBEAT — conserto ACOM 12/10 (D3)",
        "pasta": FRONT,
        "at": datetime.now().isoformat(timespec="seconds"),
        "statute": "REAL (sha256 medidos por este script no momento indicado)",
        "producao_intocada": {k: v for k, v in externals.items()},
        "copia_modificada_igual_a_producao": {
            "iald_web_server.py": externals["producao/iald_web_server.py"].get("sha256") == next(f["sha256"] for f in files if f["path"] == "copia/projetos_pyhton/IALD/iald_web_server.py"),
            "iald_app_memory.py": externals["producao/iald_app_memory.py"].get("sha256") == next(f["sha256"] for f in files if f["path"] == "copia/projetos_pyhton/IALD/iald_app_memory.py"),
        },
        "testes": None if results is None else {"all_pass": results["all_pass"], "total_cases": results["total_cases"], "failed_cases": results["failed_cases"],
                                                 "guard_events": results["guard_events"], "at": results["at"]},
        "arquivos": files,
    }
    out = os.path.join(FRONT, "MANIFESTO.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    print("files:", len(files), "manifest:", out, "sha256:", sha256(out))
    print("producao == original?", {k: externals[k]["sha256"][:16] for k in ("producao/iald_web_server.py", "producao/iald_app_memory.py")})


if __name__ == "__main__":
    main()
