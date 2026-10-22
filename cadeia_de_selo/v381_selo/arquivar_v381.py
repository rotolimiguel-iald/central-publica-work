# -*- coding: utf-8 -*-
"""Arquiva o pacote v381 (scripts, JSONs, snippets, stdouts da cadeia) em C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v381 e v381_selo,
no molde da v379 (sem o candidato de 33 MB, sem PDFs/tex/txt/logs do ensaio). Cópia byte a byte conferida; MANIFESTO_ARQUIVO_v381.json com sha256.
Rodar DEPOIS da cadeia pós-rito, do handoff e do registro no mapa. Idempotente (substitui só se os bytes diferirem; nunca apaga)."""
import os, sys, json, hashlib, shutil, time
sys.stdout.reconfigure(encoding="utf-8")
SP = r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad"
DEST = r"C:\IALD\Central de Patentes\work\cadeia_de_selo"
EXCL_EXT = {".pdf", ".tex", ".txt_", ".log", ".aux", ".out", ".toc"}
EXCL_NAME = {"um_v381_candidato.py", "carregar_embutido.py"}
MAX_B = 5 * 1024 * 1024
man = {"quando": time.strftime("%Y-%m-%d %H:%M:%S"), "arquivos": {}}
for sub in ("v381", "v381_selo"):
    src = os.path.join(SP, sub); dst = os.path.join(DEST, sub); os.makedirs(dst, exist_ok=True)
    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d not in ("__pycache__", "ensaio_superficies", "conferidor_tmp") and not d.startswith("dry")]
        for fn in files:
            p = os.path.join(root, fn); rel = os.path.relpath(p, src); ext = os.path.splitext(fn)[1].lower()
            txt_ok = ext == ".txt" and ("stdout" in fn or "_out" in fn or fn in ("AFERIDOR_v381.txt", "rito_horarios_v381.txt"))
            if fn in EXCL_NAME or ext in EXCL_EXT or (ext == ".txt" and not txt_ok):
                continue
            b = open(p, "rb").read()
            if len(b) > MAX_B:
                print("pulado (>5 MB):", sub, rel); continue
            q = os.path.join(dst, rel); os.makedirs(os.path.dirname(q), exist_ok=True)
            if os.path.exists(q) and open(q, "rb").read() == b:
                estado = "igual"
            else:
                tmp = q + ".tmp"; open(tmp, "wb").write(b); assert open(tmp, "rb").read() == b; os.replace(tmp, q); estado = "copiado"
            man["arquivos"][sub + "/" + rel.replace("\\", "/")] = {"sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b), "estado": estado}
mp = os.path.join(DEST, "v381_selo", "MANIFESTO_ARQUIVO_v381.json")
open(mp + ".tmp", "wb").write(json.dumps(man, ensure_ascii=False, indent=1).encode("utf-8")); os.replace(mp + ".tmp", mp)
print("arquivados:", sum(1 for v in man["arquivos"].values() if v["estado"] == "copiado"), "copiados;", sum(1 for v in man["arquivos"].values() if v["estado"] == "igual"), "iguais;", mp)
