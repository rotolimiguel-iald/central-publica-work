# -*- coding: utf-8 -*-
"""Monta a arvore de COPIA para refazer o reensaio otico R2 (V4 + runner R2) dentro de 5_R2/3_AUD_REPRO/copia.
Copia de BYTES dos arquivos congelados/lidos pelo runner (a R1 e o ADENDO ficam intactos). Uso: ... <saida.json>"""
import hashlib
import json
import os
import shutil
import sys

W = r"C:\IALD\Central de Patentes\work\tempo_santo_12out"
C = W + r"\5_R2\3_AUD_REPRO\copia"
pares = [
    (W + r"\1_PREREGISTRO\FREEZE.json", C + r"\1_PREREGISTRO\FREEZE.json"),
    (W + r"\2_OPTICO\RESULTADO_OPTICO.json", C + r"\2_OPTICO\RESULTADO_OPTICO.json"),
    (W + r"\2_OPTICO\ACHADOS_FORA_DO_PREREGISTRO.json", C + r"\2_OPTICO\ACHADOS_FORA_DO_PREREGISTRO.json"),
    (W + r"\2_OPTICO\run_optico.py", C + r"\2_OPTICO\run_optico.py"),
    (W + r"\2_OPTICO\diagnostico\DIAGNOSTICO_T9c.json", C + r"\2_OPTICO\diagnostico\DIAGNOSTICO_T9c.json"),
    (W + r"\5_R2\2_REENSAIO\reensaio_r2.py", C + r"\5_R2\2_REENSAIO\reensaio_r2.py"),
    (W + r"\5_R2\0_ADENDO\scripts\tolerancia_uniforme_r2.py", C + r"\5_R2\2_REENSAIO\scripts\tolerancia_uniforme_r2.py"),
    (W + r"\2_OPTICO\run_optico.py", C + r"\5_R2\2_REENSAIO\2_OPTICO\run_optico.py"),
]
# a pasta 0_ADENDO inteira (congelada): o runner le FREEZE_R2.json, ADENDO_R2.*, saidas/*, scripts/*
for dp, dn, fn in os.walk(W + r"\5_R2\0_ADENDO"):
    for f in fn:
        src = os.path.join(dp, f)
        rel = os.path.relpath(src, W + r"\5_R2\0_ADENDO")
        pares.append((src, os.path.join(C + r"\5_R2\0_ADENDO", rel)))
out = []
for src, dst in pares:
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)
    hs = hashlib.sha256(open(src, "rb").read()).hexdigest()
    hd = hashlib.sha256(open(dst, "rb").read()).hexdigest()
    out.append({"src": src, "dst": dst, "sha256": hs, "igual": hs == hd})
json.dump({"n": len(out), "todos_iguais": all(o["igual"] for o in out), "arquivos": out}, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), "arquivos copiados; iguais:", all(o["igual"] for o in out))
