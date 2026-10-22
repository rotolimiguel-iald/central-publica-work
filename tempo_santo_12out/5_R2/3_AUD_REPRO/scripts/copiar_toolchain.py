# -*- coding: utf-8 -*-
"""Copia o toolchain Lean v4.31.0 do elan para o sandbox do auditor de reproducao (so leitura na origem).
Uso: python -I -X utf8 copiar_toolchain.py <saida.json>"""
import datetime
import json
import os
import shutil
import sys
import time

SRC = r"C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0"
DST = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\5_R2\3_AUD_REPRO\sandbox\toolchain\leanprover--lean4---v4.31.0"
LONG = "\\\\?\\"  # prefixo de caminho longo do Windows: \\?\

t0 = time.time()
shutil.copytree(LONG + SRC, LONG + DST)
n = sum(len(f) for _, _, f in os.walk(LONG + DST))
out = {"src": SRC, "dst": DST, "arquivos": n, "segundos": round(time.time() - t0, 1),
       "quando_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), indent=1)
print(json.dumps(out))
