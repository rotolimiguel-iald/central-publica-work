# Confere (so leitura) as 4 superficies de memoria: acrescimo puro desde 10/10 (cada .bak_* recente e PREFIXO EXATO do atual)
import glob
import hashlib
import json
import os
import re
import sys
import time

S = [r"C:\IALD\Central de Patentes\memory\TGL_ATLAS.md", r"C:\IALD\Central de Patentes\memory\TGL_INDICE_VIVO.md",
     r"C:\IALD\Central de Patentes\memory\TGL_CORE_MEMORY.md",
     r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\AVISO_GERENCIA.md"]
T0 = time.mktime((2026, 10, 10, 0, 0, 0, 0, 0, -1))
res = []
for p in S:
    cur = open(p, "rb").read()
    st = os.stat(p)
    baks = sorted(glob.glob(p + ".bak_*"), key=os.path.getmtime)
    rec = [b for b in baks if os.path.getmtime(b) >= T0]
    e = {"arquivo": p, "bytes": len(cur), "sha256": hashlib.sha256(cur).hexdigest(),
         "mtime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(st.st_mtime)), "backups_total": len(baks),
         "backups_desde_10out": []}
    for b in rec:
        bb = open(b, "rb").read()
        pref = cur.startswith(bb)
        tail = cur[len(bb):] if pref else b""
        e["backups_desde_10out"].append({"backup": os.path.basename(b), "mtime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(b))),
                                        "bytes": len(bb), "prefixo_exato": pref, "acrescimo_bytes": (len(cur) - len(bb)) if pref else None,
                                        "marcadores_acrescidos": [m.decode() for m in re.findall(rb"<!--\s*([A-Za-z0-9_\-\.]+)\s*-->", tail)]})
    res.append(e)
    print(os.path.basename(p), e["bytes"], e["mtime"], e["sha256"][:16], "backups desde 10/10:", len(rec),
          "todos prefixo exato:", all(x["prefixo_exato"] for x in e["backups_desde_10out"]))
json.dump(res, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
