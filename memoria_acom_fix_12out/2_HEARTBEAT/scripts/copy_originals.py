# -*- coding: utf-8 -*-
"""Copia de BYTES dos originais de producao para a pasta da frente HEARTBEAT, com sha256 medido.

Nao toca producao: so leitura. Grava em originais\\ (base do diff) e em copia\\ (arvore espelho, a editar)
e em tests\\app\\ (copias para a suite existente). Registra evidencias\\ORIGINAIS_12out.json.
"""
import hashlib, json, os, shutil, sys, time
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROD = r"C:\IALD\projetos_pyhton\IALD"
LIB = r"C:\IALD\MEMORIA_IALD\lib\iald_memory"
DEPLOY = r"C:\IALD\Central de Patentes\work\iald_memoria_acom_20261010"

APP_FILES = ["iald_web_server.py", "iald_app_memory.py", "iald_app_providers.py", "iald_auto_router.py",
             "iald_task_bridge.py", "iald_memoria_operador.py", "iald_motores.py", "iald_jev_control.py"]
LIB_FILES = ["store.py", "__init__.py"]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def newline_profile(path):
    raw = open(path, "rb").read()
    crlf = raw.count(b"\r\n")
    lf = raw.count(b"\n") - crlf
    return {"bytes": len(raw), "crlf": crlf, "lf_only": lf, "bom": raw.startswith(b"\xef\xbb\xbf")}


def copy_bytes(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    raw = open(src, "rb").read()
    tmp = dst + ".tmp_copy"
    with open(tmp, "wb") as out:
        out.write(raw); out.flush(); os.fsync(out.fileno())
    if open(tmp, "rb").read() != raw:
        os.remove(tmp); raise OSError("copy verification failed: " + dst)
    os.replace(tmp, dst)
    return sha256(dst)


def main():
    receipt = {"at": datetime.now().isoformat(timespec="seconds"), "statute": "REAL (bytes lidos e copiados por este script)",
               "production_untouched": True, "files": []}
    deploy = json.load(open(os.path.join(DEPLOY, "APP_DEPLOYMENT.json"), encoding="utf-8"))
    declared = {os.path.basename(f["target"]): f["sha256"] for f in deploy["files"]}
    for name in APP_FILES:
        src = os.path.join(PROD, name)
        s = sha256(src)
        st = os.stat(src)
        entry = {"name": name, "source": src, "sha256": s, "mtime": datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds"),
                 "newline": newline_profile(src), "matches_APP_DEPLOYMENT": declared.get(name) == s}
        targets = [os.path.join(ROOT, "tests", "app", name)]
        if name in ("iald_web_server.py", "iald_app_memory.py"):
            targets.append(os.path.join(ROOT, "originais", name))
            targets.append(os.path.join(ROOT, "copia", "projetos_pyhton", "IALD", name))
        entry["copies"] = []
        for t in targets:
            if copy_bytes(src, t) != s:
                raise OSError("sha mismatch after copy: " + t)
            entry["copies"].append(t)
        receipt["files"].append(entry)
    for name in LIB_FILES:
        src = os.path.join(LIB, name)
        s = sha256(src)
        t = os.path.join(ROOT, "tests", "core", "iald_memory", name)
        if copy_bytes(src, t) != s:
            raise OSError("sha mismatch after copy: " + t)
        receipt["files"].append({"name": "iald_memory/" + name, "source": src, "sha256": s, "copies": [t],
                                 "newline": newline_profile(src)})
    # suite existente (31 casos) — copia para reescrita de 1 caso
    src = os.path.join(DEPLOY, "app", "test_app_memory.py")
    s = sha256(src)
    t = os.path.join(ROOT, "tests", "app", "test_app_memory.py")
    if not os.path.exists(t):      # a copia recebe a reescrita de 1 caso (D3); nunca sobrescrever uma copia ja editada
        copy_bytes(src, t)
    receipt["files"].append({"name": "test_app_memory.py (suite APP 31, 10/10)", "source": src, "sha256": s, "copies": [t]})
    out = os.path.join(ROOT, "evidencias", "ORIGINAIS_12out.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(receipt, f, ensure_ascii=False, indent=1)
    for e in receipt["files"]:
        print(e["name"], e["sha256"][:16], e.get("newline"), e.get("matches_APP_DEPLOYMENT", ""))
    print("receipt:", out)


if __name__ == "__main__":
    main()
